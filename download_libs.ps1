# Download Frontend Dependencies
# @author LiuHuiYu

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Downloading frontend libraries..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$libsDir = Join-Path $scriptDir "static\js\libs"
$cssDir = Join-Path $scriptDir "static\css"

# Create directories
if (!(Test-Path $libsDir)) {
    Write-Host "Creating: $libsDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $libsDir | Out-Null
}

if (!(Test-Path $cssDir)) {
    Write-Host "Creating: $cssDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $cssDir | Out-Null
}

# Download list
$downloads = @(
    @{
        Url = "https://unpkg.com/vue@3/dist/vue.global.js"
        Path = Join-Path $libsDir "vue.global.js"
        Name = "Vue.js"
    },
    @{
        Url = "https://unpkg.com/element-plus/dist/index.css"
        Path = Join-Path $cssDir "element-plus.css"
        Name = "Element Plus CSS"
    },
    @{
        Url = "https://unpkg.com/element-plus"
        Path = Join-Path $libsDir "element-plus.js"
        Name = "Element Plus JS"
    },
    @{
        Url = "https://unpkg.com/axios/dist/axios.min.js"
        Path = Join-Path $libsDir "axios.min.js"
        Name = "Axios"
    },
    @{
        Url = "https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"
        Path = Join-Path $libsDir "echarts.min.js"
        Name = "ECharts"
    },
    @{
        Url = "https://unpkg.com/@wangeditor/editor@latest/dist/css/style.css"
        Path = Join-Path $cssDir "wangeditor.css"
        Name = "WangEditor CSS"
    },
    @{
        Url = "https://unpkg.com/@wangeditor/editor@latest/dist/index.js"
        Path = Join-Path $libsDir "wangeditor.js"
        Name = "WangEditor JS"
    }
)

# Download each file
$index = 1
foreach ($item in $downloads) {
    Write-Host "[$($index)/$($downloads.Count)] Downloading $($item.Name)..." -ForegroundColor Yellow
    
    try {
        Invoke-WebRequest -Uri $item.Url -OutFile $item.Path -UseBasicParsing
        Write-Host "  [OK] $($item.Path)" -ForegroundColor Green
    }
    catch {
        Write-Host "  [FAIL] $($item.Name)" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please check your network connection and try again." -ForegroundColor Red
        Write-Host "Press any key to exit..." -ForegroundColor Red
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
    
    $index++
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Download completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Downloaded files:" -ForegroundColor White
foreach ($item in $downloads) {
    Write-Host "  [OK] $($item.Path)" -ForegroundColor Green
}
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
