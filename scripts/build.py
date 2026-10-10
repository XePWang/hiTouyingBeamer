import argparse
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = {'starter': 'starter.tex', 'example': 'example/main.tex',
             'layouts': 'example/layouts.tex'}
THEMES = ('minimalist', 'touying', 'classic')
THEME_DECLARATIONS = {
    'minimalist': r'\usetheme[minimalist]{hit}',
    'touying': r'\usetheme{hit}',
    'classic': r'\usetheme[classic]{hit}',
}
WARNING_MARKERS = ('Overfull', 'Underfull', 'Missing character', 'LaTeX Font Warning')


def compile_tex(root, source, job, out_dir, theme=None):
    root, source, out_dir = Path(root), Path(source), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if theme is not None:
        # 只生成隔离的测试入口；原始文档和正文保持不变。
        text = source.read_text(encoding='utf-8')
        decl = THEME_DECLARATIONS.get(theme, f'\\usetheme[{theme}]{{hit}}')
        text, count = re.subn(r'^[ \t]*\\usetheme(?:\[[^\]]*\])?\{hit(?:academic|minimalist)?\}',
                              lambda _: decl, text, flags=re.MULTILINE)
        if count != 1:
            raise ValueError(f'{source} 必须包含一处明确的主题声明，实际匹配到 {count} 处')
        variants = out_dir / 'sources'
        variants.mkdir(exist_ok=True)
        source = variants / f'{job}.tex'
        source.write_text(text, encoding='utf-8')
    command = ['latexmk', '-xelatex', '-interaction=nonstopmode', '-halt-on-error',
               '-file-line-error', f'-jobname={job}', f'-outdir={out_dir.as_posix()}',
               source.as_posix()]
    result = subprocess.run(command, cwd=root, capture_output=True)
    (out_dir / f'{job}-console.txt').write_bytes(result.stdout + result.stderr)
    pdf = out_dir / f'{job}.pdf'
    log = out_dir / f'{job}.log'
    if result.returncode or not pdf.is_file():
        tail = (result.stdout + result.stderr).decode('utf-8', errors='replace').splitlines()[-40:]
        raise RuntimeError(f'编译失败：{source}；查看 {out_dir / (job + "-console.txt")}\n'
                           + '\n'.join(tail))
    warnings = [line for line in log.read_text(encoding='utf-8', errors='replace').splitlines()
                if any(marker in line for marker in WARNING_MARKERS)]
    if warnings:
        raise ValueError(f'{job} 出现排版或字体告警：\n' + '\n'.join(warnings[:8]))
    return pdf


def build_document(name, theme=None, root=ROOT):
    root = Path(root)
    job = f'{name}-{theme}' if theme else name
    print(f'编译 {job}', flush=True)
    pdf = compile_tex(root, root / DOCUMENTS[name], job, root / '.work/build', theme)
    target = root / ('slides/starter.pdf' if name == 'starter' and theme is None
                     else f'examples/{job}.pdf')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf, target)
    return target


def main():
    parser = argparse.ArgumentParser(description='构建起步文档与示例')
    parser.add_argument('--document', '-d', choices=[*DOCUMENTS, 'all'], default='starter')
    parser.add_argument('--theme', choices=[*THEMES, 'all', 'both'])
    args = parser.parse_args()
    names = list(DOCUMENTS) if args.document == 'all' else [args.document]
    if args.theme in ('all', 'both'):
        themes = list(THEMES)
    elif args.theme:
        themes = [args.theme]
    else:
        themes = [None]
    for name in names:
        for theme in themes:
            print(build_document(name, theme))


if __name__ == '__main__':
    main()
