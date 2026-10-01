import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

from build import ROOT, DOCUMENTS, THEMES, build_document, compile_tex


def collect_release_files():
    # 只分发已经纳入 Git 的项目文件，未跟踪的个人资料不进入发布包。
    result = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT,
                            capture_output=True, check=True)
    names = result.stdout.decode('utf-8').rstrip('\0').split('\0')
    files = []
    for name in names:
        path = Path(name)
        if any(part in ('.git', '.work', 'dist', '__pycache__') for part in path.parts) or name == 'CHANGELOG.md':
            raise ValueError(f'本地文件不应被 Git 跟踪或发布：{name}')
        files.append(ROOT / path)
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
    for script in ('check-template.py', 'check-authoring.py'):
        subprocess.run([sys.executable, str(unpacked / 'scripts' / script)],
                       cwd=unpacked, check=True)
    authoring = json.loads((unpacked / '.work/author-check/validation.json').read_text(encoding='utf-8'))
    destination = ROOT / 'dist/hiTouyingBeamer-release.zip'
    destination.parent.mkdir(exist_ok=True)
    candidate.replace(destination)
    report = {'status': 'SUCCESS', 'documents': checks, 'authoring': authoring,
              'verification_directory': str(unpacked),
              'files': [file.relative_to(ROOT).as_posix() for file in files],
              'source_sha256': {file.relative_to(ROOT).as_posix(): hashlib.sha256(file.read_bytes()).hexdigest()
                                for file in files},
              'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}
    (work / 'release-validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'发布包已验证：{destination}')


if __name__ == '__main__':
    main()
