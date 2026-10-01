param(
  [ValidateSet('starter', 'example', 'layouts', 'all')]
  [string]$Document = 'starter'
)
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
  $OutDir = Join-Path $PSScriptRoot '.work/build'
  New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
  $Documents = if ($Document -eq 'all') { @('starter', 'example', 'layouts') } else { @($Document) }
  foreach ($doc in $Documents) {
    $source = switch ($doc) {
      'starter' { 'starter.tex' }
      'example' { 'example/main.tex' }
      'layouts' { 'example/layouts.tex' }
    }
    $target = if ($doc -eq 'starter') { 'slides/starter.pdf' } else { "example/preview/$doc.pdf" }
    Write-Host "正在编译 $source"
    latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error `
      "-jobname=$doc" "-outdir=$OutDir" $source
    if ($LASTEXITCODE -ne 0) { throw "编译失败，请查看 $OutDir/$doc.log" }
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
    Copy-Item -LiteralPath (Join-Path $OutDir "$doc.pdf") -Destination $target -Force
    Write-Host "已生成 $target"
  }
} finally {
  Pop-Location
}
