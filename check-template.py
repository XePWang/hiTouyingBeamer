import hashlib
import json
from pathlib import Path
import subprocess

from fontTools.ttLib import TTFont
from pypdf import PdfReader

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'fonts/manifest.json').read_text(encoding='utf-8'))
font_count = 0
for entry in manifest['files']:
    path = root / entry['path']
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != entry['sha256']:
        raise ValueError(f'资源校验失败：{path}')
    if path.suffix in {'.otf', '.ttf'}:
        font_count += 1
        with TTFont(path) as font:
            if font['OS/2'].fsType != entry['embedding_fsType']:
                raise ValueError(f'字体嵌入元数据发生变化：{path}')
    elif 'SIL OPEN FONT LICENSE Version 1.1' not in path.read_text(encoding='utf-8'):
        raise ValueError(f'字体许可证不完整：{path}')
if font_count != 10:
    raise ValueError(f'字体数量异常：{font_count}')

pdf = PdfReader(root / 'example.pdf')
if len(pdf.pages) != 22:
    raise ValueError(f'示例页数异常：{len(pdf.pages)}')
for number, page in enumerate(pdf.pages, 1):
    if abs(float(page.mediabox.width) / float(page.mediabox.height) - 16 / 9) > .001:
        raise ValueError(f'画幅异常：第 {number} 页')
    if not page.extract_text().strip():
        raise ValueError(f'空白页面：第 {number} 页')
log = (root / 'example.log').read_text(encoding='utf-8', errors='replace')
problems = [line for line in log.splitlines()
            if any(marker in line for marker in ['Overfull', 'Missing character', 'LaTeX Font Warning'])]
if problems:
    raise ValueError('\n'.join(problems))

font_reports = {}
for path in [root / 'example.pdf', *sorted((root / 'assets/figures').glob('*.pdf'))]:
    result = subprocess.run(['pdffonts', str(path)], capture_output=True, text=True, check=True)
    if result.stderr.strip():
        raise ValueError(f'PDF 字体检查报告异常：{path}\n{result.stderr}')
    rows = result.stdout.splitlines()[2:]
    for row in rows:
        cells = row.split()
        if cells and (cells[-5] != 'yes' or 'Type 3' in row):
            raise ValueError(f'PDF 字体嵌入异常：{row}')
        if any(name in row for name in ['Arial', 'YaHei', 'Consolas', 'Noto-Sans-SC']):
            raise ValueError(f'PDF 使用了模板字体范围外的字体：{row}')
    font_reports[path.relative_to(root).as_posix()] = rows

report = {'pages': len(pdf.pages), 'font_files': font_count,
          'licensed_resource_files': len(manifest['files']),
          'pdf_sha256': hashlib.sha256((root / 'example.pdf').read_bytes()).hexdigest(),
          'layout_warnings': problems, 'embedded_fonts': font_reports}
(root / '.work').mkdir(exist_ok=True)
(root / '.work/template-check.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'检查通过：{len(pdf.pages)} 页，{font_count} 个原始字体文件，全部 PDF 字体已嵌入。')
