import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

root = Path(__file__).resolve().parent
work = root / '.work' / 'agenda-check'
work.mkdir(parents=True, exist_ok=True)


def compile_case(name, source, definition, passes, expected_error=None):
    command = ['xelatex', '-interaction=nonstopmode', '-halt-on-error',
               '-file-line-error', f'-jobname={name}', f'-output-directory={work}',
               definition + '\\input{' + source + '}']
    for run in range(passes):
        result = subprocess.run(command, cwd=root, capture_output=True)
        (work / f'{name}-run{run + 1}.txt').write_bytes(result.stdout + result.stderr)
        if expected_error is None and result.returncode != 0:
            raise RuntimeError(f'编译失败：{name}；查看 {work / (name + ".log")}')
        if expected_error is not None:
            log = (work / f'{name}.log').read_text(encoding='utf-8', errors='replace')
            compact_log = re.sub(r'\s+', '', log)
            if result.returncode == 0 or expected_error.replace(' ', '') not in compact_log:
                raise AssertionError(f'没有按预期拒绝无效输入：{name}')
            return {'name': name, 'rejected': True, 'expected_error': expected_error}
    log = (work / f'{name}.log').read_text(encoding='utf-8', errors='replace')
    warnings = [line for line in log.splitlines() if any(
        marker in line for marker in ['Overfull', 'Missing character', 'LaTeX Font Warning'])]
    if warnings:
        raise AssertionError(f'{name}: {warnings}')
    return PdfReader(work / f'{name}.pdf')


report = {'automatic': [], 'rejected': []}
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
    links = [item.get_object() for item in page.get('/Annots', [])]
    if len(links) != 2 * count:
        raise AssertionError(f'目录跳转数量错误：{name} {len(links)}')
    for index, item in enumerate(links):
        target = item.get('/A', {}).get('/D')
        if target not in pdf.named_destinations:
            raise AssertionError(f'无效目录跳转：{name} {target}')
        if pdf.get_destination_page_number(pdf.named_destinations[target]) != index // 2 + 1:
            raise AssertionError(f'目录跳转到了错误章节：{name} {target}')
    report['automatic'].append({'items': count, 'pages': len(pdf.pages),
                                'links': len(links), 'layout_checked': True})

pdf = compile_case('agenda-two-lines', 'tests/agenda-manual.tex', '\\def\\AgendaCase{2}', 2)
if 'Controlling' not in pdf.pages[0].extract_text():
    raise AssertionError('两行英文标题缺失')
report['two_line_title'] = 'passed'
for case, message in [(0, 'received 7'), (1, 'received 1'),
                      (3, 'exceeds two lines'), (4, 'inside AgendaSlide')]:
    report['rejected'].append(compile_case(
        f'agenda-invalid-{case}', 'tests/agenda-manual.tex',
        '\\def\\AgendaCase{' + str(case) + '}', 1, message))

(work / 'validation.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('检查通过：自动目录 2–6 项、章节跳转、附录排除、两行标题与四类无效输入。')
