import hashlib
import json
import re
import subprocess
import sys

from pypdf import PdfReader
import pymupdf

from build import ROOT, DOCUMENTS, THEMES, build_document, compile_tex


def compact(text):
    return re.sub(r'\s+', '', text)


def main():
    report = {'previews': {}, 'compatibility': {}}
    for name in DOCUMENTS:
        for theme in THEMES:
            pdf = build_document(name, theme)
            report['previews'][pdf.name] = hashlib.sha256(pdf.read_bytes()).hexdigest()
    for script in ('check-template.py', 'check-navigation.py', 'check-agenda.py'):
        subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], cwd=ROOT, check=True)

    fields = {
        'starter': ['我的汇报标题', '副标题', 'PresentationTitle', '学术汇报',
                    '研究问题', '研究方法', '结果与讨论', '感谢聆听',
                    '填写本页最重要的判断', '填写有证据支持的比较结论'],
        'example': ['并行计算研究', 'PresentingParallelComputingResearch', '学术汇报模板',
                    '汇报人', '哈尔滨工业大学', '目录', '问题与模型', '实现与机制',
                    '图表与评价', '讨论与结论', 'IMPLEMENTATION', '把算法中的一次操作',
                    '落实为线程中的一次访问', 'vectoraddition', '三个阅读锚点',
                    '同一个Warp的前四个Lane', '先读趋势，再读边界',
                    '在Amdahl模型中加入额外时间', '定义问题', '解释机制', '建立证据',
                    '感谢聆听', '阅读顺序明确的三线表', '附录'],
        'layouts': ['单栏要点', '左文右图', '左图右文', '上图下文', '双图对比',
                    '双栏内容', '三栏内容', '大图加图注', '公式与符号说明',
                    '表格与说明', '代码与说明', '本页需要听众记住的结论'],
    }
    rendered = 0
    for name, expected in fields.items():
        for theme in THEMES:
            pdf = ROOT / f'example/preview/{name}-{theme}.pdf'
            text = compact('\n'.join(p.extract_text() for p in PdfReader(pdf).pages))
            missing = [item for item in expected if compact(item) not in text]
            if missing:
                raise AssertionError(f'{pdf.name} 内容缺失：{missing}')
            with pymupdf.open(pdf) as doc:
                for page in doc:
                    pix = page.get_pixmap()
                    if pix.width <= 0 or pix.height <= 0:
                        raise AssertionError(f'{pdf.name} 页面渲染失败')
                    rendered += 1

    cases = [
        ('example/agenda.tex', 'agenda', 6),
        ('example/legacy.tex', 'legacy', 28),
        ('tests/switch-hit.tex', 'switch-hit', 9),
        ('tests/switch-hitacademic.tex', 'switch-hitacademic', 7),
        ('tests/switch-madrid.tex', 'switch-madrid', 7),
        ('tests/classic-43.tex', 'classic-43', 9),
        ('tests/overlay-pages.tex', 'overlay-pages', 6),
        ('tests/if-hit-before.tex', 'if-hit-before', 11),
        ('tests/if-hit-after.tex', 'if-hit-after', 11),
        ('tests/if-hitacademic-before.tex', 'if-hitacademic-before', 9),
        ('tests/if-hitacademic-after.tex', 'if-hitacademic-after', 9),
        ('tests/if-madrid-before.tex', 'if-madrid-before', 9),
        ('tests/if-madrid-after.tex', 'if-madrid-after', 9),
        ('tests/author-images.tex', 'author-images', 3),
    ]
    for source, job, pages in cases:
        print(f'检查 {job}', flush=True)
        pdf = compile_tex(ROOT, ROOT / source, job, ROOT / '.work/compatibility')
        reader = PdfReader(pdf)
        if len(reader.pages) != pages:
            raise AssertionError(f'{job} 页数变化：{len(reader.pages)}，期望 {pages}')
        if job == 'classic-43':
            box = reader.pages[0].mediabox
            if abs(float(box.width) / float(box.height) - 4 / 3) > .001:
                raise AssertionError('4:3 页面比例错误')
        report['compatibility'][job] = pages
    subprocess.run([sys.executable, str(ROOT / 'scripts/check-authoring.py')], cwd=ROOT, check=True)
    report['authoring'] = json.loads((ROOT / '.work/author-check/validation.json').read_text(encoding='utf-8'))
    report.update(status='SUCCESS', rendered_preview_pages=rendered)
    (ROOT / '.work/test-summary.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'通过：六份预览共 {rendered} 页，{len(cases)} 项兼容用例，目录边界与链接检查。')


if __name__ == '__main__':
    main()
