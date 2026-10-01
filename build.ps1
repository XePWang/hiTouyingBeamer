param([ValidateSet('example', 'starter', 'agenda-gallery')][string]$Document = 'example')
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error "$Document.tex"
    if ($LASTEXITCODE -ne 0) { throw "编译失败：$Document.log" }
    Write-Host "已生成 $Document.pdf"
} finally {
    Pop-Location
}
