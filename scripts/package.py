import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

from build import ROOT, DOCUMENTS, THEMES, build_document, compile_tex


def collect_release_files():
    files = [ROOT / name for name in ('README.md', 'LICENSE', '.gitignore',
                                     'starter.tex', 'build.ps1')]
    files.extend(ROOT.glob('*.sty'))
    extensions = {'.tex', '.md', '.txt', '.json', '.py', '.ps1', '.mjs', '.yml',
                  '.pdf', '.png', '.jpg', '.jpeg', '.otf', '.ttf', '.mmd'}
    for directory in ('slides', 'example', 'docs', 'scripts', 'tests', 'fonts',
                      'assets', 'vi', '.github'):
        for file in (ROOT / directory).rglob('*'):
            if not file.is_file() or file.suffix.lower() not in extensions:
                continue
            if '__pycache__' in file.parts:
                continue
            relative = file.relative_to(ROOT).as_posix()
            if relative in ('slides/starter.pdf', 'example/preview/starter.pdf',
                            'example/preview/example.pdf', 'example/preview/layouts.pdf'):
                continue
            files.append(file)
    for file in files:
        if not file.is_file():
            raise FileNotFoundError(file)
    return sorted(set(files))


def main():
    for name in DOCUMENTS:
        for theme in THEMES:
            build_document(name, theme)
    files = collect_release_files()
    work = ROOT / '.work'
    work.mkdir(exist_ok=True)
    # 每次使用全新目录，保留验证证据，不递归删除已有工作。
    verify = Path(tempfile.mkdtemp(prefix='release-', dir=work))
    candidate = verify / 'candidate.zip'
    with zipfile.ZipFile(candidate, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, 'hiTouyingBeamer/' + file.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(candidate) as archive:
        archive.extractall(verify)
    unpacked = verify / 'hiTouyingBeamer'
    checks = []
    for name, source in DOCUMENTS.items():
        for theme in THEMES:
            job = f'{name}-{theme}'
            print(f'独立解压验证 {job}', flush=True)
            compile_tex(unpacked, unpacked / source, job, unpacked / '.work/build', theme)
            checks.append(job)
    destination = ROOT / 'dist/hiTouyingBeamer-release.zip'
    destination.parent.mkdir(exist_ok=True)
    candidate.replace(destination)
    report = {'status': 'SUCCESS', 'documents': checks,
              'verification_directory': str(unpacked),
              'files': [file.relative_to(ROOT).as_posix() for file in files],
              'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}
    (work / 'release-validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'发布包已验证：{destination}')


if __name__ == '__main__':
    main()
