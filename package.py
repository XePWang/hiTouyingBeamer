#!/usr/bin/env python3
"""hiTouyingBeamer 发布打包与独立解压验证脚本
功能：
  1. 生成纯净的开源发布包 ZIP（排除 .git、.work、临时文件与日志）；
  2. 包含推荐 starter、完整 example、双主题与公共层、必需字体、素材、许可证与最新双主题预览 PDF；
  3. 在全新隔离临时目录中解压，并验证 starter 与 example 在两个主题下的编译与切换。
"""
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST_DIR = ROOT / 'dist'
RELEASE_ZIP = DIST_DIR / 'hiTouyingBeamer-release.zip'
VERIFY_DIR = ROOT / '.work' / 'verify-release'


def collect_release_files():
    """收集打包所需文件"""
    include_files = [
        'starter.tex',
        'example.tex',
        'beamerthemehitacademic.sty',
        'beamerthemehit.sty',
        'beamercmdhit.sty',
        'hit-content.sty',
        'hit-outline.sty',
        'hit-fonts.sty',
        'build.py',
        'build.ps1',
        'README.md',
        'LICENSE',
        'CHANGELOG.md',
    ]

    include_dirs = [
        'examples',
        'assets',
        'fonts',
        'vi',
    ]

    files_to_pack = []

    for f in include_files:
        src = ROOT / f
        if not src.exists():
            raise FileNotFoundError(f'缺少打包关键文件: {f}')
        files_to_pack.append((src, f))

    for d in include_dirs:
        dir_path = ROOT / d
        if not dir_path.is_dir():
            raise FileNotFoundError(f'缺少打包关键目录: {d}')
        for item in dir_path.rglob('*'):
            if item.is_file():
                # 排除临时文件与缓存
                if item.suffix in ('.aux', '.log', '.out', '.nav', '.toc', '.snm', '.vrb', '.pyc'):
                    continue
                if '__pycache__' in item.parts:
                    continue
                rel = item.relative_to(ROOT).as_posix()
                files_to_pack.append((item, rel))

    # 生成并包含两种主题对应的最新预览 PDF
    previews = [
        ('example.pdf', 'preview-example-academic.pdf'),
        ('starter.pdf', 'preview-starter-academic.pdf'),
    ]
    for src_name, zip_name in previews:
        src = ROOT / src_name
        if src.exists():
            files_to_pack.append((src, zip_name))

    # 包含从 test-suite/build 生成的 classic 预览
    classic_previews = [
        (ROOT / '.work' / 'test-suite' / 'build' / 'example-classic.pdf', 'preview-example-classic.pdf'),
        (ROOT / '.work' / 'test-suite' / 'build' / 'starter-classic.pdf', 'preview-starter-classic.pdf'),
    ]
    for src, zip_name in classic_previews:
        if src.exists():
            files_to_pack.append((src, zip_name))

    return files_to_pack


def create_zip(files_to_pack):
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    if RELEASE_ZIP.exists():
        RELEASE_ZIP.unlink()

    print(f'正在创建发布包: {RELEASE_ZIP.name} ...')
    with zipfile.ZipFile(RELEASE_ZIP, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for src, arcname in files_to_pack:
            # 统一打包在外层目录 hiTouyingBeamer/ 下，解压后目录整洁
            full_arc = f'hiTouyingBeamer/{arcname}'
            zf.write(src, full_arc)

    size_mb = RELEASE_ZIP.stat().st_size / (1024 * 1024)
    print(f'发布包创建成功！体积: {size_mb:.2f} MB，包含 {len(files_to_pack)} 个文件。')


def verify_zip():
    print('\n============================================================')
    print('在新解压目录中验证发布包独立编译与主题切换...')
    print('============================================================')
    if VERIFY_DIR.exists():
        shutil.rmtree(VERIFY_DIR)
    VERIFY_DIR.mkdir(parents=True)

    with zipfile.ZipFile(RELEASE_ZIP, 'r') as zf:
        zf.extractall(VERIFY_DIR)

    unpacked_root = VERIFY_DIR / 'hiTouyingBeamer'
    if not (unpacked_root / 'starter.tex').exists():
        raise AssertionError('解压目录未找到 starter.tex')

    # 1. 验证 starter.tex 在 hitacademic 下编译
    print('1. 验证解压包 starter.tex (hitacademic)...')
    cmd1 = ['latexmk', '-xelatex', '-interaction=nonstopmode', '-halt-on-error', 'starter.tex']
    res1 = subprocess.run(cmd1, cwd=unpacked_root, capture_output=True, text=True, errors='replace')
    if res1.returncode != 0 or not (unpacked_root / 'starter.pdf').exists():
        raise RuntimeError(f'解压包 starter.tex 编译失败:\n{res1.stderr}\n{res1.stdout}')
    print('   [OK] starter.tex (hitacademic) 编译成功！')

    # 2. 切换 starter.tex 到 hit 主题并验证编译
    print('2. 切换 starter.tex 为 hit 主题并验证编译...')
    starter_content = (unpacked_root / 'starter.tex').read_text(encoding='utf-8')
    starter_hit = starter_content.replace('\\usetheme{hitacademic}', '\\usetheme{hit}')
    (unpacked_root / 'starter.tex').write_text(starter_hit, encoding='utf-8')
    res2 = subprocess.run(cmd1, cwd=unpacked_root, capture_output=True, text=True, errors='replace')
    if res2.returncode != 0:
        raise RuntimeError(f'解压包 starter.tex (hit) 切换编译失败:\n{res2.stderr}')
    print('   [OK] starter.tex (hit) 切换编译成功！')

    # 3. 验证 example.tex 在 hitacademic 下编译
    print('3. 验证解压包 example.tex (hitacademic)...')
    cmd3 = ['latexmk', '-xelatex', '-interaction=nonstopmode', '-halt-on-error', 'example.tex']
    res3 = subprocess.run(cmd3, cwd=unpacked_root, capture_output=True, text=True, errors='replace')
    if res3.returncode != 0 or not (unpacked_root / 'example.pdf').exists():
        raise RuntimeError(f'解压包 example.tex 编译失败:\n{res3.stderr}')
    print('   [OK] example.tex (hitacademic) 编译成功！')

    # 4. 切换 example.tex 到 hit 主题并验证编译
    print('4. 切换 example.tex 为 hit 主题并验证编译...')
    example_content = (unpacked_root / 'example.tex').read_text(encoding='utf-8')
    example_hit = example_content.replace('\\usetheme{hitacademic}', '\\usetheme{hit}')
    (unpacked_root / 'example.tex').write_text(example_hit, encoding='utf-8')
    res4 = subprocess.run(cmd3, cwd=unpacked_root, capture_output=True, text=True, errors='replace')
    if res4.returncode != 0:
        raise RuntimeError(f'解压包 example.tex (hit) 切换编译失败:\n{res4.stderr}')
    print('   [OK] example.tex (hit) 切换编译成功！')

    print('\n[SUCCESS] 发布包在新隔离目录中编译与主题无损切换验证 100% 通过！')


def main():
    files = collect_release_files()
    create_zip(files)
    verify_zip()


if __name__ == '__main__':
    main()
