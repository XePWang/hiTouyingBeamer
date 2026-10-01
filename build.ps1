param(
  [ValidateSet('example', 'starter', 'agenda-gallery', 'legacy-classic',
    'theme-switch-hit', 'theme-switch-hitacademic', 'theme-switch-madrid')]
  [string]$Document = 'example'
)
$ErrorActionPreference = 'Stop'
# 编译产物统一放在工作目录：本机 TeX Live 的启动脚本不接受含中文的输出目录，
# 因此输出目录固定用 .work/w 这个短路径，仓库根目录只留源码与分发用的 PDF。
New-Item -ItemType Directory -Force -Path '.work/w' | Out-Null
$source = switch ($Document) {
  'legacy-classic' { 'examples/legacy-classic.tex' }
  'theme-switch-hit' { 'tests/switch-hit.tex' }
  'theme-switch-hitacademic' { 'tests/switch-hitacademic.tex' }
  'theme-switch-madrid' { 'tests/switch-madrid.tex' }
  default { "$Document.tex" }
}
$job = [System.IO.Path]::GetFileNameWithoutExtension($source)
# 分发的文件名与源文件同名；主题切换的三个变体加 theme-switch- 前缀，
# 这样能一眼看出它们是同一份正文换了主题。
$target = switch ($Document) {
  'theme-switch-hit' { 'theme-switch-hit.pdf' }
  'theme-switch-hitacademic' { 'theme-switch-hitacademic.pdf' }
  'theme-switch-madrid' { 'theme-switch-madrid.pdf' }
  default { "$job.pdf" }
}
Push-Location $PSScriptRoot
try {
  # latexmk 负责多遍编译：目录页与章节导航需要两遍以上才能稳定。
  # -outdir 的值必须是字面量，写成变量会被原样传给 latexmk。
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error `
    '-outdir=.work/w' $source
  if ($LASTEXITCODE -ne 0) { throw "编译失败：$job.log" }
  # 分发的 PDF 统一放在仓库根目录，和源码同级，便于直接打开。
  Copy-Item (Join-Path '.work/w' "$job.pdf") $target -Force
  Write-Host "已生成 $target"
} finally {
  Pop-Location
}
