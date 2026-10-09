import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
work = root / '.work' / 'agenda-check'
build = work / 'build'
if build.exists():
    if not build.resolve().is_relative_to((root / '.work').resolve()):
        raise ValueError('测试清理路径超出 .work')
    shutil.rmtree(build)
build.mkdir(parents=True)

# 复制样式包与资源目录到构建沙箱
for package in sorted(root.glob('*.sty')):
    shutil.copy2(package, build / package.name)
for directory in ('fonts', 'assets', 'vi'):
    source_dir = root / directory
    if source_dir.is_dir():
        shutil.copytree(source_dir, build / directory)
(build / 'tests').mkdir()
for source in sorted((root / 'tests').glob('*.tex')):
    shutil.copy2(source, build / 'tests' / source.name)

env = dict(os.environ)
env['TEXINPUTS'] = str(root) + os.pathsep

WARNINGS = ['Overfull', 'Missing character']


def run_xelatex(name, source, definition, passes, halt=False):
    command = ['xelatex', '-interaction=nonstopmode', '-file-line-error',
               f'-jobname={name}',
               definition + '\\input{' + source + '}']
    if halt:
        command.insert(2, '-halt-on-error')
    results = []
    for run in range(passes):
        result = subprocess.run(command, cwd=build, capture_output=True, env=env)
        (work / f'{name}-run{run + 1}.txt').write_bytes(result.stdout + result.stderr)
        results.append(result)
    return results


def compile_case(name, source, definition, passes, expected_error=None):
    results = run_xelatex(name, source, definition, passes,
                          halt=expected_error is None)
    log = (build / f'{name}.log').read_text(encoding='utf-8', errors='replace')
    if expected_error is not None:
        compact_log = re.sub(r'\s+', '', log)
        if results[-1].returncode == 0 or expected_error.replace(' ', '') not in compact_log:
            raise AssertionError(f'没有按预期拒绝无效输入：{name}')
        return {'name': name, 'rejected': True, 'expected_error': expected_error}
    if results[-1].returncode != 0:
        raise RuntimeError(f'编译失败：{name}；查看 {work / (name + f"-run{passes}.txt")}')
    warnings = [line for line in log.splitlines()
                if any(marker in line for marker in WARNINGS)]
    if warnings:
        raise AssertionError(f'{name} 出现排版告警: {warnings[:3]}')
    return PdfReader(build / f'{name}.pdf')


def link_targets(page, pdf):
    """返回页面上每个链接的目标命名目标及其对应的 1-based 页码。

    严格解析真实跳转目标：
    1. 禁止将裸数字字符串直接作为页码（禁止 target.isdigit()）；
    2. 目标必须在 pdf.named_destinations 中存在；
    3. 解析其对应的精确目的页码。
    """
    targets = []
    annots = page.get('/Annots')
    if not annots:
        return []
    for item in annots.get_object():
        action = item.get_object().get('/A')
        if not action:
            continue
        target = action.get_object().get('/D')
        if not isinstance(target, str):
            raise AssertionError(f'无法识别的跳转目标：{target}')
        if target.isdigit():
            raise AssertionError(f'禁止使用纯数字字符串作为命名目标：{target}')
        if target not in pdf.named_destinations:
            raise AssertionError(f'命名目标在 PDF 中不存在：{target}')
        dest_obj = pdf.named_destinations[target]
        target_page = pdf.get_destination_page_number(dest_obj) + 1
        targets.append((target, target_page))
    return targets


def expected_section_pages(count):
    r"""tests/agenda-auto.tex 的结构：
    <= 6 章节时目录占 1 页，章节首页从第 2 页开始；
    > 6 章节时目录均分占 2 页，章节首页从第 3 页开始。
    """
    if count <= 0:
        return []
    toc_pages = 1 if count <= 6 else (count + 5) // 6
    return [toc_pages + i for i in range(1, count + 1)]


def check_links_exact(name, pdf, count, toc_page_count, is_block):
    """核对目录跳转：链接数量、目标真实存在、且页码 1:1 精确匹配章节起始页。"""
    targets = []
    for p_idx in range(toc_page_count):
        targets.extend(link_targets(pdf.pages[p_idx], pdf))

    expected_links_count = (2 * count) if is_block else count
    if len(targets) != expected_links_count:
        raise AssertionError(
            f'目录跳转数量错误：{name} 期望 {expected_links_count}，实际 {len(targets)}')

    expected_pages = expected_section_pages(count)
    if is_block:
        for idx in range(count):
            num_tgt, num_page = targets[2 * idx]
            tl_tgt, tl_page = targets[2 * idx + 1]
            if num_page != expected_pages[idx] or tl_page != expected_pages[idx]:
                raise AssertionError(
                    f'目录跳转目标未精确对应章节首页：{name} 第 {idx+1} 章期望 {expected_pages[idx]}，'
                    f'实际 {num_page}/{tl_page}')
    else:
        for idx in range(count):
            tgt, page_num = targets[idx]
            if page_num != expected_pages[idx]:
                raise AssertionError(
                    f'目录跳转目标未精确对应章节首页：{name} 第 {idx+1} 章期望 {expected_pages[idx]}，'
                    f'实际 {page_num}')

    resolved_pages = [t[1] for t in targets]
    if resolved_pages != sorted(resolved_pages):
        raise AssertionError(f'目录跳转顺序与章节顺序不一致：{name} {resolved_pages}')
    return targets, expected_pages


report = {
    'counts_tested': [],
    'automatic': [],
    'list_layout': [],
    'zero_section': None,
    'first_run': None,
    'classic': None,
    'manual_target': None,
    'two_line_title': None,
    'rejected': []
}

ALL_SECTION_TITLES = [
    '研究背景', '问题定义', '研究方法', '实现过程', '实验评价', '结论展望',
    '第七章节', '第八章节', '第九章节'
]

# -------------------------------------------------- 1. 零章节测试 ====
print('--> 验证 0 章节自动目录')
pdf0 = compile_case('agenda-auto-0', 'tests/agenda-auto.tex', '\\def\\AgendaCount{0}', 2)
p0_text = pdf0.pages[0].extract_text()
if '未检测到章节' not in p0_text:
    raise AssertionError('0 章节时未给出明确的未检测到章节状态')
targets0 = link_targets(pdf0.pages[0], pdf0)
if len(targets0) != 0:
    raise AssertionError('0 章节时目录不应产生跳转链接')
report['zero_section'] = {'pages': len(pdf0.pages), 'state': '未检测到章节'}
report['counts_tested'].append(0)

# -------------------------------------------------- 2. 自动目录 1 项 ====
print('--> 验证 1 章节列表版式')
pdf1 = compile_case('agenda-auto-1', 'tests/agenda-auto.tex', '\\def\\AgendaCount{1}', 3)
p1_text = pdf1.pages[0].extract_text()
if '研究背景' not in p1_text or '01' not in p1_text:
    raise AssertionError('1 章节自动目录未显示标题或编号')
targets1, home1 = check_links_exact('agenda-auto-1', pdf1, 1, toc_page_count=1, is_block=False)
report['list_layout'].append({'items': 1, 'pages': len(pdf1.pages), 'targets': targets1})
report['counts_tested'].append(1)

# -------------------------------------------------- 3. 自动目录 2–6 项（版块版式） ====
for count in range(2, 7):
    print(f'--> 验证 {count} 章节版块版式')
    name = f'agenda-auto-{count}'
    pdf = compile_case(name, 'tests/agenda-auto.tex', '\\def\\AgendaCount{' + str(count) + '}', 3)
    text = pdf.pages[0].extract_text()
    for idx in range(count):
        title = ALL_SECTION_TITLES[idx]
        if title not in text:
            raise AssertionError(f'{name} 缺少章节标题：{title}')
    if '附录' in text:
        raise AssertionError(f'{name} 目录混入了附录章节')
    targets, homes = check_links_exact(name, pdf, count, toc_page_count=1, is_block=True)
    report['automatic'].append({
        'items': count, 'pages': len(pdf.pages), 'layout': 'block',
        'targets': targets, 'expected_pages': homes
    })
    report['counts_tested'].append(count)

# -------------------------------------------------- 4. 自动目录 >6 项（列表分页版式：7、9 项） ====
for count in (7, 9):
    print(f'--> 验证 {count} 章节多页列表版式（防截断与分页）')
    name = f'agenda-auto-{count}'
    pdf = compile_case(name, 'tests/agenda-auto.tex', '\\def\\AgendaCount{' + str(count) + '}', 3)
    toc_text = pdf.pages[0].extract_text() + '\n' + pdf.pages[1].extract_text()
    for idx in range(count):
        title = ALL_SECTION_TITLES[idx]
        if title not in toc_text:
            raise AssertionError(f'{name} 列表版式缺少章节标题：{title}')
    if '附录' in toc_text:
        raise AssertionError(f'{name} 列表版式混入附录章节')
    targets, homes = check_links_exact(name, pdf, count, toc_page_count=2, is_block=False)
    report['list_layout'].append({
        'items': count, 'pages': len(pdf.pages), 'layout': 'list-multipage',
        'targets': targets, 'expected_pages': homes
    })
    report['counts_tested'].append(count)

# -------------------------------------------------- 5. 首次编译状态测试 ====
print('--> 验证首次编译提示状态')
results = run_xelatex('agenda-first-run', 'tests/agenda-auto.tex', '\\def\\AgendaCount{4}', 1)
log_first = (build / 'agenda-first-run.log').read_text(encoding='utf-8', errors='replace')
pdf_first = PdfReader(build / 'agenda-first-run.pdf')
if '重新运行一次编译即可读取章节标题' not in pdf_first.pages[0].extract_text():
    raise AssertionError('首次编译未在目录页显示明确重新运行提示')
report['first_run'] = 'passed'

# -------------------------------------------------- 6. 手动目录与跳转 ====
print('--> 验证手动目录两行标题与编号')
pdf_man2 = compile_case('agenda-two-lines', 'tests/agenda-manual.tex', '\\def\\AgendaCase{2}', 2)
man2_text = pdf_man2.pages[0].extract_text()
if 'Controlling' not in man2_text or '01' not in man2_text or '02' not in man2_text:
    raise AssertionError('手动目录两行标题或编号缺失')
report['two_line_title'] = 'passed'

print('--> 验证手动目录显式目标精确跳转')
pdf_mantgt = compile_case('agenda-manual-target', 'tests/agenda-manual.tex', '\\def\\AgendaCase{5}', 2)
mantargets = link_targets(pdf_mantgt.pages[0], pdf_mantgt)
if len(mantargets) != 4:
    raise AssertionError(f'手动目录显式跳转数量错误：{len(mantargets)}')
if mantargets[0][1] != mantargets[1][1] or mantargets[2][1] != mantargets[3][1]:
    raise AssertionError(f'同一条目的编号与标题跳转目标页码不一致：{mantargets}')
if mantargets[0][1] >= mantargets[2][1]:
    raise AssertionError(f'手动目录跳转目标顺序颠倒：{mantargets}')
report['manual_target'] = {'targets': mantargets}

# -------------------------------------------------- 7. 手动目录非法输入拒绝 ====
print('--> 验证手动目录边界与非法输入防御')
for case, message in [(0, 'received 7'), (1, 'received 1'),
                      (3, 'exceeds two lines'), (4, 'AgendaSlide')]:
    report['rejected'].append(compile_case(
        f'agenda-invalid-{case}', 'tests/agenda-manual.tex',
        '\\def\\AgendaCase{' + str(case) + '}', 1, message))

# -------------------------------------------------- 8. 经典主题目录与子章节 ====
print('--> 验证经典主题目录与子章节层级')
pdf_classic = compile_case('agenda-classic-outline', 'tests/agenda-classic.tex', '', 3)
classic_text = pdf_classic.pages[0].extract_text()
if '不进入主目录' not in classic_text:
    raise AssertionError('经典主题目录未正确渲染子章节')
if '目录' not in classic_text:
    raise AssertionError('经典主题目录标题缺失')
classic_targets = link_targets(pdf_classic.pages[0], pdf_classic)
if len(classic_targets) < 3:
    raise AssertionError(f'经典主题目录跳转数量异常：{len(classic_targets)}')
report['classic'] = {'pages': len(pdf_classic.pages), 'targets': classic_targets}

# -------------------------------------------------- 9. 附录与过渡页综合验证 ====
print('--> 验证附录内容完整性与排除规则')
pdf_app = compile_case('agenda-appendix', 'tests/agenda-auto.tex', '\\def\\AgendaCount{4}', 3)
app_text = pdf_app.pages[-1].extract_text()
if 'Appendix' not in app_text and '附录' not in app_text:
    raise AssertionError('附录页内容丢失')

(work / 'validation.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('\n[SUCCESS] 目录系统全部测试通过！')
print(f'实际覆盖章节数用例: {report["counts_tested"]}')
print('包含：0 章节空状态、1 章节列表、2–6 章节双胶囊、7 与 9 章节多页防截断列表、'
      '目标严格为有效命名目标且 1:1 精确匹配章节起始页、子章节层级、附录隔离、以及 4 类输入防御。')
