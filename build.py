#!/usr/bin/env python3
"""hiTouyingBeamer 跨平台构建脚本
支持构建单个目标或全部发布成品。
用法：
  python build.py --document example
  python build.py --document all
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / '.work' / 'w'

DOCUMENTS = {
    'example': ('example.tex', 'example.pdf'),
    'starter': ('starter.tex', 'starter.pdf'),
    'agenda-gallery': ('agenda-gallery.tex', 'agenda-gallery.pdf'),
    'legacy-classic': ('examples/legacy-classic.tex', 'legacy-classic.pdf'),
    'theme-switch-hit': ('tests/switch-hit.tex', 'theme-switch-hit.pdf'),
    'theme-switch-hitacademic': ('tests/switch-hitacademic.tex', 'theme-switch-hitacademic.pdf'),
    'theme-switch-madrid': ('tests/switch-madrid.tex', 'theme-switch-madrid.pdf'),
}


def build_document(doc_key: str) -> None:
    if doc_key not in DOCUMENTS:
        raise ValueError(f'未知文档目标: {doc_key}，可用目标: {list(DOCUMENTS.keys())}')

    source_rel, target_rel = DOCUMENTS[doc_key]
    source_path = ROOT / source_rel
    target_path = ROOT / target_rel
    job_name = Path(source_rel).stem

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f'正在编译: {source_rel} -> {target_rel}')

    cmd = [
        'latexmk',
        '-xelatex',
        '-interaction=nonstopmode',
        '-halt-on-error',
        '-file-line-error',
        f'-outdir={OUT_DIR.as_posix()}',
        str(source_path.as_posix()),
    ]
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        raise RuntimeError(f'编译失败: {job_name}.log，查看 .work/w/{job_name}.log')

    compiled_pdf = OUT_DIR / f'{job_name}.pdf'
    if not compiled_pdf.exists():
        raise FileNotFoundError(f'未找到生成的 PDF: {compiled_pdf}')

    shutil.copy2(compiled_pdf, target_path)
    print(f'已生成: {target_rel}')


def main():
    parser = argparse.ArgumentParser(description='hiTouyingBeamer 构建入口')
    parser.add_argument(
        '--document',
        '-d',
        choices=['all', *DOCUMENTS.keys()],
        default='example',
        help='需要构建的文档（默认: example，支持 all 构建全部）',
    )
    args = parser.parse_args()

    targets = list(DOCUMENTS.keys()) if args.document == 'all' else [args.document]
    for target in targets:
        build_document(target)
    print('\n构建完成！')


if __name__ == '__main__':
    main()
