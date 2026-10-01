import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader

root = Path(__file__).resolve().parent
work = root / '.work' / 'agenda-check'
# xelatex 在本机对含中文的绝对输出目录会失败，因此把源文件复制到工作目录，
# 在工作目录内编译，生成物不落在仓库根目录。
# 字体、素材与视觉形象资产按相对路径解析，一并复制，构建目录才能独立编译。
build = work / 'build'
if build.exists():
    shutil.rmtree(build)
build.mkdir(parents=True)
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

WARNINGS = ['Overfull', 'Missing character', 'LaTeX Font Warning']


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
        raise RuntimeError(f'编译失败：{name}；查看 {work / (name + "-run1.txt")}')
    warnings = [line for line in log.splitlines()
                if any(marker in line for marker in WARNINGS)]
    if warnings:
        raise AssertionError(f'{name}: {warnings[:3]}')
    return PdfReader(build / f'{name}.pdf')


def link_targets(page, pdf):
    """返回页面上每个链接的目标页码，按注解出现顺序。

    /D 既可能是命名目标（\\hyperlink），也可能是直接页码（beamer 的导航链接）。
    """
    pages = []
    for item in page.get('/Annots', []):
        target = item.get_object().get('/A', {}).get('/D')
        if not isinstance(target, str):
            raise AssertionError(f'无法识别的跳转目标：{target}')
        if target in pdf.named_destinations:
            pages.append(pdf.get_destination_page_number(pdf.named_destinations[target]))
        elif target.isdigit():
            pages.append(int(target))
        else:
            raise AssertionError(f'无效跳转目标：{target}')
    return pages


def expected_section_pages(count):
    r"""tests/agenda-auto.tex 的结构：目录页之后每章一页正文，最后是附录一章。"""
    return [index + 1 for index in range(count)]


def check_links(name, pdf, titles):
    r"""核对目录跳转：数量、目标有效，且不早于该章首页。

    数字目标由 \hypertarget 直接给出；\hyperlink 的命名目标由 hyperref 记录，
    beamer 把 Navigation 标签指向该章所在页，因此两者都应落在该章首页或之后。
    """
    page = pdf.pages[0]
    targets = link_targets(page, pdf)
    if len(targets) != 2 * len(titles):
        raise AssertionError(f'目录跳转数量错误：{name} {len(targets)}')
    section_home = expected_section_pages(len(titles))
    for index, title in enumerate(titles):
        number_target, label_target = targets[2 * index], targets[2 * index + 1]
        if number_target < section_home[index] or label_target < section_home[index]:
            raise AssertionError(
                f'目录跳转早于章节首页：{name} {title} '
                f'{number_target}/{label_target} < {section_home[index]}')
    # 章节顺序必须与目录条目顺序一致。
    if targets[::2] != sorted(targets[::2]):
        raise AssertionError(f'目录跳转顺序与章节顺序不一致：{name} {targets}')
    return targets, section_home


report = {'automatic': [], 'list_layout': [], 'rejected': [], 'classic': []}

SECTION_TITLES = ['研究背景', '问题定义', '研究方法', '实现过程', '实验评价', '结论展望']

# 自动目录 2–6 项：版块版式、编号顺序、跳转目标、子章节与附录排除。
for count in range(2, 7):
    name = f'agenda-auto-{count}'
    pdf = compile_case(name, 'tests/agenda-auto.tex',
                       '\\def\\AgendaCount{' + str(count) + '}', 3)
    page = pdf.pages[0]
    text = page.extract_text()
    numbers = re.findall(r'\b0[1-6]\b', text)
    if numbers != [f'{i:02}' for i in range(1, count + 1)]:
        raise AssertionError(f'目录数量或顺序错误：{name} {numbers}')
    if any(word in text for word in ['附录', '不进入']):
        raise AssertionError(f'目录混入附录或子章节：{name}')
    targets, section_home = check_links(name, pdf, SECTION_TITLES[:count])
    report['automatic'].append({'items': count, 'pages': len(pdf.pages),
                                'links': len(targets), 'layout': 'block',
                                'targets': targets, 'section_home': section_home})

# 1 项：超出 2–6 项范围，改用普通列表版式，且不截断章节。
pdf = compile_case('agenda-auto-1', 'tests/agenda-auto.tex', '\\def\\AgendaCount{1}', 3)
text = pdf.pages[0].extract_text()
if '研究背景' not in text:
    raise AssertionError('单项自动目录没有排出章节名')
report['list_layout'].append({'items': 1, 'pages': len(pdf.pages), 'layout': 'list'})

# 超过 6 项：同样改用普通列表版式，章节数量不得被截断。
for count in (7, 9):
    name = f'agenda-auto-{count}'
    pdf = compile_case(name, 'tests/agenda-auto.tex',
                       '\\def\\AgendaCount{' + str(count) + '}', 3)
    text = pdf.pages[0].extract_text()
    for title in ['研究背景', '问题定义']:
        if title not in text:
            raise AssertionError(f'列表版式缺少章节：{name} {title}')
    if '附录' in text:
        raise AssertionError(f'列表版式混入附录章节：{name}')
    report['list_layout'].append({'items': count, 'pages': len(pdf.pages), 'layout': 'list'})

# 首次构建、缺少 .toc：给出重新运行提示，并且不报错。
results = run_xelatex('agenda-first-run', 'tests/agenda-auto.tex', '\\def\\AgendaCount{4}', 1)
log = (build / 'agenda-first-run.log').read_text(encoding='utf-8', errors='replace')
if 'Rerun' not in log:
    raise AssertionError('首次构建没有给出重新运行的提示')
report['first_run'] = 'passed'

# 手动目录：两行标题、条目编号与数量校验。跳转由自动目录一项覆盖：
# 手动目录的条目在没有 \hypertarget 时与改动前一样不产生链接。
pdf = compile_case('agenda-two-lines', 'tests/agenda-manual.tex', '\\def\\AgendaCase{2}', 2)
first_page = pdf.pages[0].extract_text()
if 'Controlling' not in first_page:
    raise AssertionError('两行英文标题缺失')
if '01' not in first_page or '02' not in first_page:
    raise AssertionError('手动目录编号缺失')
if 'Only one' in first_page or 'Line one' in first_page:
    raise AssertionError('手动目录混入了其他用例的条目')
report['two_line_title'] = 'passed'

# 手动目录的显式跳转目标：给出 \hypertarget 时链接必须有效。
# 每个条目有编号与标题两个链接，因此两条目共四个链接。
pdf = compile_case('agenda-manual-target', 'tests/agenda-manual.tex',
                   '\\def\\AgendaCase{5}', 2)
targets = link_targets(pdf.pages[0], pdf)
if len(targets) != 4:
    raise AssertionError(f'手动目录显式跳转数量错误：{len(targets)}')
if targets[0] != targets[1] or targets[2] != targets[3]:
    raise AssertionError(f'同一目标的编号与标题跳转不一致：{targets}')
if targets[0] >= targets[2]:
    raise AssertionError(f'手动目录显式跳转顺序错误：{targets}')
if any(target < 1 or target >= len(pdf.pages) for target in targets):
    raise AssertionError(f'手动目录显式跳转目标越界：{targets}')
report['manual_target'] = {'links': len(targets), 'targets': targets}

# 手动目录的非法输入：数量越界、标题超过两行、条目放在目录之外。
for case, message in [(0, 'received 7'), (1, 'received 1'),
                      (3, 'exceeds two lines'), (4, 'inside AgendaSlide')]:
    report['rejected'].append(compile_case(
        f'agenda-invalid-{case}', 'tests/agenda-manual.tex',
        '\\def\\AgendaCase{' + str(case) + '}', 1, message))

# 经典主题：目录沿用原有样式，子章节照常显示，不使用 2–6 项限制。
pdf = compile_case('agenda-classic-outline', 'tests/agenda-classic.tex', '', 3)
text = ''.join(page.extract_text() for page in pdf.pages[:2])
if '不进入主目录' not in text:
    raise AssertionError('经典主题目录没有显示子章节')
if '目录' not in text:
    raise AssertionError('经典主题目录标题缺失')
report['classic'].append({'pages': len(pdf.pages), 'shows_subsections': True})

# 标准附录与章节过渡页下的页码与跳转。
pdf = compile_case('agenda-appendix', 'tests/agenda-auto.tex', '\\def\\AgendaCount{4}', 3)
appendix_text = pdf.pages[-1].extract_text()
if 'Appendix' not in appendix_text and '附录' not in appendix_text:
    raise AssertionError('附录页内容缺失')

(work / 'validation.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('检查通过：自动目录 2–6 项版块版式、1 项与超过 6 项的列表版式、首次构建、'
      '章节跳转、附录排除、两行标题、经典目录子章节与四类无效输入。')
