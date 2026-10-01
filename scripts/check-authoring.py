import argparse
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from pypdf import PdfReader
import pymupdf

from build import ROOT, THEMES, compile_tex


def check_document_links(root):
    parser = MarkdownIt()
    count = 0
    sources = [root / 'README.md', *sorted((root / 'docs').glob('*.md')),
               *sorted((root / 'example').rglob('*.md'))]
    for source in sources:
        for token in parser.parse(source.read_text(encoding='utf-8')):
            for child in token.children or []:
                if child.type != 'link_open':
                    continue
                link = urlsplit(child.attrGet('href'))
                if link.scheme or link.netloc or not link.path:
                    continue
                target = (source.parent / unquote(link.path)).resolve()
                if not target.is_relative_to(root.resolve()) or not target.exists():
                    raise AssertionError(f'文档链接不可用：{source.relative_to(root)} -> {link.path}')
                count += 1
    return count


def luminance(rgb):
    values = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
    return sum(c * w for c, w in zip(values, (.2126, .7152, .0722)))


def check_visibility(pdf):
    boxes = 0
    images = 0
    with pymupdf.open(pdf) as doc:
        for page in doc:
            # 曲线区域的包围盒不代表实际填充区域，只检查实心矩形内容框。
            backgrounds = [d for d in page.get_drawings()
                           if d['fill'] is not None and d['fill_opacity'] >= .99
                           and len(d['items']) == 1 and d['items'][0][0] == 're']
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        bounds = pymupdf.Rect(span['bbox'])
                        candidates = [d for d in backgrounds if d['rect'].contains(bounds)]
                        if not candidates or not span['text'].strip():
                            continue
                        background = min(candidates, key=lambda d: d['rect'].get_area())
                        # 只核对文字后的小型实色框，封面和整页背景留给目视检查。
                        if background['rect'].get_area() > page.rect.get_area() / 3:
                            continue
                        value = span['color']
                        fg = ((value >> 16 & 255) / 255, (value >> 8 & 255) / 255, (value & 255) / 255)
                        a, b = sorted((luminance(fg), luminance(background['fill'])))
                        if (b + .05) / (a + .05) < 3:
                            raise AssertionError(f'{pdf.name} 第 {page.number + 1} 页文字与背景接近：{span["text"]}')
                        boxes += 1
            for info in page.get_image_info():
                bounds = pymupdf.Rect(info['bbox'])
                # 模板装饰可超出页面边界；核对正文中的完整图片。
                if bounds.y0 < 55 or not page.rect.contains(bounds):
                    continue
                original = info['width'] / info['height']
                displayed = bounds.width / bounds.height
                if abs(displayed / original - 1) > .01:
                    raise AssertionError(f'{pdf.name} 第 {page.number + 1} 页图片变形')
                images += 1
            page.get_pixmap()
    return {'visible_text_spans': boxes, 'proportional_images': images}


def check_workflow(pdf):
    reader = PdfReader(pdf)
    text = re.sub(r'\s+', '', '\n'.join(p.extract_text() for p in reader.pages))
    expected = ('作者操作流程示例', '示例作者', '示例单位', '汇报提纲',
                '输入与目标', '横图与说明', '竖图与横图对比', '比较采用相同的输入范围')
    missing = [item for item in expected if item not in text]
    if missing:
        raise AssertionError(f'{pdf.name} 缺少正文：{missing}')
    toc = reader.pages[1]
    for item in ('问题范围', '线性函数', '平方函数'):
        if item not in re.sub(r'\s+', '', toc.extract_text()):
            raise AssertionError(f'{pdf.name} 目录缺少子章节：{item}')
    targets = []
    for annotation in toc.get('/Annots', []):
        action = annotation.get_object().get('/A')
        if not action or action.get('/S') != '/GoTo':
            continue
        name = action.get('/D')
        if name not in reader.named_destinations:
            raise AssertionError(f'{pdf.name} 无效目录跳转：{name}')
        targets.append(reader.get_destination_page_number(reader.named_destinations[name]) + 1)
    if targets != [3, 3, 4, 4, 5, 5]:
        raise AssertionError(f'{pdf.name} 章节和子章节跳转不符：{targets}')
    result = check_visibility(pdf)
    if result['visible_text_spans'] < 2 or result['proportional_images'] < 2:
        raise AssertionError(f'{pdf.name} 未实际覆盖结论文字与图片检查')
    return {'pages': len(reader.pages), 'toc_targets': targets, **result}


def main():
    parser = argparse.ArgumentParser(description='检查作者流程与文档链接')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    out = root / '.work/author-check'
    report = {'links': check_document_links(root), 'themes': {}, 'rejected': []}
    for theme in THEMES:
        pdf = compile_tex(root, root / 'tests/author-workflow.tex',
                          f'author-workflow-{theme}', out, theme)
        report['themes'][theme] = check_workflow(pdf)
        for name in ('starter', 'layouts', 'example'):
            check_visibility(root / f'example/preview/{name}-{theme}.pdf')
    for case, message in [(0, 'Column ratio'), (1, 'Column ratio'), (2, 'missing-author-image')]:
        job = f'author-error-{case}'
        result = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error',
                                 f'-jobname={job}', f'-output-directory={out.relative_to(root).as_posix()}',
                                 f'\\def\\AuthorCase{{{case}}}\\input{{tests/author-errors.tex}}'],
                                cwd=root, capture_output=True)
        (out / f'{job}-console.txt').write_bytes(result.stdout + result.stderr)
        log = (out / f'{job}.log').read_text(encoding='utf-8', errors='replace')
        if result.returncode == 0 or message not in log:
            raise AssertionError(f'未按预期拒绝输入 {case}')
        report['rejected'].append(case)
    report['status'] = 'SUCCESS'
    (out / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                                         encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
