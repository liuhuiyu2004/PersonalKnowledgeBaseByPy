@echo off
echo ========================================
echo   个人知识库系统 - 安装脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 检查 Python 版本...
python --version

echo.
echo [2/4] 创建虚拟环境...
python -m venv venv

echo.
echo [3/4] 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [4/4] 创建配置文件...
if not exist .env (
    copy .env.example .env
    echo 已创建 .env 配置文件，请根据需求修改配置
) else (
    echo .env 文件已存在，跳过
)

echo.
echo ========================================
echo   安装完成!
echo ========================================
echo.
echo 下一步:
echo 1. 编辑 .env 文件配置你的 API 密钥 (可选)
echo 2. 运行 start.bat 启动服务
echo.
pause
