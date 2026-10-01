import hashlib
import json
import subprocess
from pathlib import Path

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

# 需要分发的 PDF、页数、画幅，以及是否必须只用随模板分发的字体。
# 画幅用宽高比表示，169 为 16:9，43 为 4:3。
# 页数不是判定兼容的依据，只用于发现结构被意外改动。
# 经典主题的文档没有写 fontset=none，中文用系统字体，因此不限制字体来源。
DOCUMENTS = {
    'example.pdf': (22, 16 / 9, True),
    'starter.pdf': (7, 16 / 9, True),
    'agenda-gallery.pdf': (6, 16 / 9, True),
    'legacy-classic.pdf': (28, 16 / 9, False),
    'theme-switch-hit.pdf': (9, 16 / 9, False),
    'theme-switch-hitacademic.pdf': (7, 16 / 9, True),
    'theme-switch-madrid.pdf': (7, 16 / 9, False),
}
# 出现这些字体说明文档落到了系统字体上；只对要求自带字体的文档检查。
FORBIDDEN = ['Arial', 'YaHei', 'Consolas', 'Noto-Sans-SC', 'SimSun', 'SimHei']
WARNING_MARKERS = ['Overfull', 'Underfull', 'Missing character', 'LaTeX Font Warning']

report = {'documents': {}, 'font_files': font_count,
          'licensed_resource_files': len(manifest['files'])}

for name, (expected_pages, expected_ratio, bundled_only) in DOCUMENTS.items():
    path = root / name
    if not path.exists():
        raise ValueError(f'缺少需要分发的 PDF：{name}，先运行 build.ps1')
    pdf = PdfReader(path)
    if len(pdf.pages) != expected_pages:
        raise ValueError(f'{name} 页数异常：{len(pdf.pages)}，期望 {expected_pages}')
    for number, page in enumerate(pdf.pages, 1):
        box = page.mediabox
        ratio = float(box.width) / float(box.height)
        if abs(ratio - expected_ratio) > .001:
            raise ValueError(f'{name} 画幅异常：第 {number} 页')
        if not page.extract_text().strip():
            raise ValueError(f'{name} 空白页面：第 {number} 页')
    log = root / '.work' / 'w' / name.replace('.pdf', '.log')
    problems = []
    if log.exists():
        text = log.read_text(encoding='utf-8', errors='replace')
        problems = [line for line in text.splitlines()
                    if any(marker in line for marker in WARNING_MARKERS)]
    if problems:
        raise ValueError(f'{name} 编译日志有告警：\n' + '\n'.join(problems[:5]))

    fonts = {}
    for target in [path, *sorted((root / 'assets/figures').glob('*.pdf'))]:
        result = subprocess.run(['pdffonts', str(target)], capture_output=True, text=True, check=True)
        if result.stderr.strip():
            raise ValueError(f'PDF 字体检查报告异常：{target}\n{result.stderr}')
        rows = result.stdout.splitlines()[2:]
        for row in rows:
            cells = row.split()
            if cells and (cells[-5] != 'yes' or 'Type 3' in row):
                raise ValueError(f'PDF 字体嵌入异常：{row}')
            if bundled_only and any(font in row for font in FORBIDDEN):
                raise ValueError(f'PDF 使用了模板字体范围外的字体：{row}')
        fonts[target.relative_to(root).as_posix()] = rows
    report['documents'][name] = {
        'pages': len(pdf.pages),
        'ratio': round(expected_ratio, 4),
        'pdf_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'embedded_fonts': fonts,
    }

(root / '.work').mkdir(exist_ok=True)
(root / '.work/template-check.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'检查通过：{len(DOCUMENTS)} 个 PDF 页数与画幅正确、字体全部嵌入，'
      f'{font_count} 个原始字体文件校验一致。')
