param(
  [ValidateSet('all', 'example', 'starter', 'agenda-gallery', 'legacy-classic',
    'theme-switch-hit', 'theme-switch-hitacademic', 'theme-switch-madrid')]
  [string]$Document = 'example'
)
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
  # 编译中间产物统一保存在 .work/w 临时目录中，保持仓库根目录干净
  $OutDir = Join-Path $PSScriptRoot '.work/w'
  if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
  }

  $DocList = if ($Document -eq 'all') {
    @('example', 'starter', 'agenda-gallery', 'legacy-classic',
      'theme-switch-hit', 'theme-switch-hitacademic', 'theme-switch-madrid')
  } else {
    @($Document)
  }

  foreach ($doc in $DocList) {
    $source = switch ($doc) {
      'legacy-classic' { 'examples/legacy-classic.tex' }
      'theme-switch-hit' { 'tests/switch-hit.tex' }
      'theme-switch-hitacademic' { 'tests/switch-hitacademic.tex' }
      'theme-switch-madrid' { 'tests/switch-madrid.tex' }
      default { "$doc.tex" }
    }
    $job = [System.IO.Path]::GetFileNameWithoutExtension($source)
    $target = switch ($doc) {
      'theme-switch-hit' { 'theme-switch-hit.pdf' }
      'theme-switch-hitacademic' { 'theme-switch-hitacademic.pdf' }
      'theme-switch-madrid' { 'theme-switch-madrid.pdf' }
      default { "$job.pdf" }
    }

    Write-Host "正在编译: $source -> $target"
    latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error `
      "-outdir=$OutDir" $source
    if ($LASTEXITCODE -ne 0) { throw "编译失败：$job.log" }

    $compiledPdf = Join-Path $OutDir "$job.pdf"
    $destPdf = Join-Path $PSScriptRoot $target
    Copy-Item $compiledPdf $destPdf -Force
    Write-Host "已生成 $target"
  }
} finally {
  Pop-Location
}
