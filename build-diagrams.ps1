param(
    [string]$ChromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    [string]$MermaidCli = ''
)
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    if (-not (Test-Path -LiteralPath $ChromePath)) { throw "浏览器不存在：$ChromePath" }
    New-Item -ItemType Directory -Path .work -Force | Out-Null
    if (-not $MermaidCli) {
        $MermaidCli = Join-Path $PSScriptRoot '.work/mermaid/node_modules/@mermaid-js/mermaid-cli/src/cli.js'
        if (-not (Test-Path -LiteralPath $MermaidCli)) {
            $env:PUPPETEER_SKIP_DOWNLOAD = 'true'
            npm.cmd install --prefix .work/mermaid --cache .work/npm-cache @mermaid-js/mermaid-cli@12.0.0 --no-audit --no-fund
            if ($LASTEXITCODE -ne 0) { throw 'Mermaid CLI 安装失败' }
        }
    }
    $fontData = [Convert]::ToBase64String([IO.File]::ReadAllBytes((Join-Path $PSScriptRoot 'fonts/source-sans/SourceSans3-Regular.ttf')))
    $fontCss = "@font-face { font-family: 'Source Sans 3'; src: url(data:font/ttf;base64,$fontData) format('truetype'); }"
    [IO.File]::WriteAllText((Join-Path $PSScriptRoot '.work/diagram-fonts.css'), $fontCss)
    @{ executablePath = $ChromePath; headless = $true; args = @('--no-sandbox'); userDataDir = (Join-Path $PSScriptRoot '.work/chrome-profile') } | ConvertTo-Json | Set-Content -LiteralPath .work/puppeteer.json -Encoding UTF8
    node build-diagrams.mjs $MermaidCli
    if ($LASTEXITCODE -ne 0) { throw '流程图构建失败' }
} finally {
    Pop-Location
}
