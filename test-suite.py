#!/usr/bin/env python3
"""hiTouyingBeamer 综合自动化测试套件
执行内容：
  Stage 1: 字体元数据与发布成品检查 (check-template.py)
  Stage 2: 目录系统全功能与边界测试 (check-agenda.py)
  Stage 3: 完整正文与起步文档主题切换语义保留测试 (example.tex / starter.tex under hit & hitacademic)
  Stage 4: 辅助接口矩阵与扩展功能测试 (4:3 画幅、覆盖层、加载顺序矩阵)
  Stage 5: 页面渲染与版式健康度检查 (PyMuPDF 渲染、非空、画幅一致性)
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader
import pymupdf

ROOT = Path(__file__).resolve().parent
WORK_DIR = ROOT / '.work' / 'test-suite'
OUT_DIR = WORK_DIR / 'build'


def run_cmd(cmd, cwd=ROOT):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors='replace')


def stage_1_template_check():
    print('\n============================================================')
    print('Stage 1: 运行 check-template.py 发布成品与字体检查')
    print('============================================================')
    res = run_cmd([sys.executable, str(ROOT / 'check-template.py')])
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
        raise RuntimeError('Stage 1 失败：check-template.py 未通过')
    print(res.stdout.strip())
    print('[PASS] Stage 1 校验通过！')


def stage_2_agenda_check():
    print('\n============================================================')
    print('Stage 2: 运行 check-agenda.py 目录系统全面回归测试')
    print('============================================================')
    res = run_cmd([sys.executable, str(ROOT / 'check-agenda.py')])
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
        raise RuntimeError('Stage 2 失败：check-agenda.py 未通过')
    print(res.stdout.strip())
    print('[PASS] Stage 2 校验通过！')


def compile_tex(source_path: Path, job_name: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        'latexmk',
        '-xelatex',
        '-interaction=nonstopmode',
        '-halt-on-error',
        '-file-line-error',
        f'-jobname={job_name}',
        f'-outdir={out_dir.as_posix()}',
        str(source_path.as_posix()),
    ]
    res = run_cmd(cmd, cwd=ROOT)
    log_file = out_dir / f'{job_name}.log'
    if res.returncode != 0 or not (out_dir / f'{job_name}.pdf').exists():
        log_snippet = ''
        if log_file.exists():
            log_snippet = '\n'.join(log_file.read_text(encoding='utf-8', errors='replace').splitlines()[-30:])
        raise RuntimeError(f'编译失败: {job_name}\n{log_snippet}')

    # 检查日志是否存在排版告警
    if log_file.exists():
        text = log_file.read_text(encoding='utf-8', errors='replace')
        warnings = [l for l in text.splitlines() if any(m in l for m in ['Overfull', 'Underfull', 'Missing character', 'LaTeX Font Warning'])]
        if warnings:
            raise ValueError(f'{job_name} 日志存在告警:\n' + '\n'.join(warnings[:5]))

    return out_dir / f'{job_name}.pdf'


def stage_3_semantic_check():
    print('\n============================================================')
    print('Stage 3: 验证完整文档在两种主题下的无损切换与语义保留')
    print('============================================================')
    # 1. 验证 starter.tex
    starter_src = ROOT / 'starter.tex'
    starter_text = starter_src.read_text(encoding='utf-8')
    starter_acad_tex = WORK_DIR / 'starter-academic.tex'
    starter_hit_tex = WORK_DIR / 'starter-classic.tex'
    starter_acad_tex.write_text(starter_text, encoding='utf-8')
    starter_hit_tex.write_text(starter_text.replace('\\usetheme{hitacademic}', '\\usetheme{hit}'), encoding='utf-8')

    pdf_s_acad = compile_tex(starter_acad_tex, 'starter-academic', OUT_DIR)
    pdf_s_hit = compile_tex(starter_hit_tex, 'starter-classic', OUT_DIR)

    starter_fields = [
        '我的汇报标题', '副标题', 'PresentationTitle', '学术汇报',
        '汇报人', '目录', '研究问题', '研究方法', '结果与讨论', '感谢聆听',
        '填写本页最重要的判断', '填写有证据支持的比较结论'
    ]
    t_s_acad = re.sub(r'\s+', '', '\n'.join(p.extract_text() for p in PdfReader(pdf_s_acad).pages))
    t_s_hit = re.sub(r'\s+', '', '\n'.join(p.extract_text() for p in PdfReader(pdf_s_hit).pages))
    for f in starter_fields:
        cf = re.sub(r'\s+', '', f)
        if cf not in t_s_acad or cf not in t_s_hit:
            raise AssertionError(f'starter.tex 字段缺失：{f} (acad={cf in t_s_acad}, hit={cf in t_s_hit})')
    print('  [OK] starter.tex 在 hit 与 hitacademic 下 100% 字段对齐！')

    # 2. 验证 example.tex
    example_src = ROOT / 'example.tex'
    example_text = example_src.read_text(encoding='utf-8')
    example_acad_tex = WORK_DIR / 'example-academic.tex'
    example_hit_tex = WORK_DIR / 'example-classic.tex'
    example_acad_tex.write_text(example_text, encoding='utf-8')
    example_hit_tex.write_text(example_text.replace('\\usetheme{hitacademic}', '\\usetheme{hit}'), encoding='utf-8')

    pdf_e_acad = compile_tex(example_acad_tex, 'example-academic', OUT_DIR)
    pdf_e_hit = compile_tex(example_hit_tex, 'example-classic', OUT_DIR)

    example_fields = [
        '并行计算研究', 'PresentingParallelComputingResearch', '学术汇报模板',
        '汇报人', '哈尔滨工业大学', '目录', '问题与模型', '实现与机制', '图表与评价', '讨论与结论',
        'IMPLEMENTATION', '把算法中的一次操作', '落实为线程中的一次访问',
        'vectoraddition', '三个阅读锚点', '同一个Warp的前四个Lane',
        '先读趋势，再读边界', '在Amdahl模型中加入额外时间', '定义问题', '解释机制', '建立证据',
        '感谢聆听', '阅读顺序明确的三线表', '附录'
    ]
    t_e_acad = re.sub(r'\s+', '', '\n'.join(p.extract_text() for p in PdfReader(pdf_e_acad).pages))
    t_e_hit = re.sub(r'\s+', '', '\n'.join(p.extract_text() for p in PdfReader(pdf_e_hit).pages))
    for f in example_fields:
        cf = re.sub(r'\s+', '', f)
        if cf not in t_e_acad or cf not in t_e_hit:
            raise AssertionError(f'example.tex 字段缺失：{f} (acad={cf in t_e_acad}, hit={cf in t_e_hit})')
    print('  [OK] example.tex 在 hit 与 hitacademic 下 100% 字段对齐，零排版告警！')
    print('[PASS] Stage 3 校验通过！')


def stage_4_auxiliary_check():
    print('\n============================================================')
    print('Stage 4: 运行 4:3 画幅、覆盖层与接口加载顺序矩阵测试')
    print('============================================================')
    aux_tests = [
        ('tests/classic-43.tex', 'classic-43', 9),
        ('tests/overlay-pages.tex', 'overlay-pages', 6),
        ('tests/if-hit-before.tex', 'if-hit-before', 11),
        ('tests/if-hit-after.tex', 'if-hit-after', 11),
        ('tests/if-hitacademic-before.tex', 'if-hitacademic-before', 9),
        ('tests/if-hitacademic-after.tex', 'if-hitacademic-after', 9),
        ('tests/if-madrid-before.tex', 'if-madrid-before', 9),
        ('tests/if-madrid-after.tex', 'if-madrid-after', 9),
    ]
    for rel_path, job, expected_pages in aux_tests:
        pdf_path = compile_tex(ROOT / rel_path, job, OUT_DIR)
        reader = PdfReader(pdf_path)
        if len(reader.pages) != expected_pages:
            raise AssertionError(f'{job} 页数不符：期望 {expected_pages}，实际 {len(reader.pages)}')
        if job == 'classic-43':
            box = reader.pages[0].mediabox
            ratio = float(box.width) / float(box.height)
            if abs(ratio - 4/3) > 0.01:
                raise AssertionError(f'classic-43 画幅异常：{ratio}')
        print(f'  [OK] {job} ({len(reader.pages)} 页，无告警)')
    print('[PASS] Stage 4 校验通过！')


def stage_5_render_check():
    print('\n============================================================')
    print('Stage 5: 页面像素级光栅化与版式健康度检查 (PyMuPDF)')
    print('============================================================')
    all_pdfs = [
        ROOT / 'example.pdf',
        ROOT / 'starter.pdf',
        ROOT / 'agenda-gallery.pdf',
        ROOT / 'legacy-classic.pdf',
        ROOT / 'theme-switch-hit.pdf',
        ROOT / 'theme-switch-hitacademic.pdf',
        ROOT / 'theme-switch-madrid.pdf',
        OUT_DIR / 'example-classic.pdf',
        OUT_DIR / 'starter-classic.pdf',
    ]
    total_pages = 0
    for pdf_path in all_pdfs:
        doc = pymupdf.open(str(pdf_path))
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            pix = page.get_pixmap()
            if pix.width <= 0 or pix.height <= 0:
                raise AssertionError(f'{pdf_path.name} 第 {page_idx+1} 页光栅化失败尺寸非法')
            total_pages += 1
        print(f'  [OK] {pdf_path.name}: {len(doc)} 页全部正常光栅化')
    print(f'[PASS] Stage 5 校验通过！共核验 {total_pages} 个渲染页面。')


def main():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    report = {'status': 'RUNNING'}
    try:
        stage_1_template_check()
        stage_2_agenda_check()
        stage_3_semantic_check()
        stage_4_auxiliary_check()
        stage_5_render_check()

        report['status'] = 'SUCCESS'
        (WORK_DIR / 'test-summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print('\n' + '=' * 60)
        print('【所有测试全部通过！ALL TESTS PASSED】')
        print('=' * 60)
    except Exception as e:
        report['status'] = 'FAILED'
        report['error'] = str(e)
        (WORK_DIR / 'test-summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
