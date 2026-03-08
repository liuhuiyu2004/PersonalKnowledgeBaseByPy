@echo off
echo ========================================
echo   启动个人知识库系统
echo ========================================
echo.

REM 激活虚拟环境
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [警告] 未找到虚拟环境，将使用全局 Python
)

echo 正在启动服务...
echo 访问 http://127.0.0.1:8000 使用 Web 界面
echo 访问 http://127.0.0.1:8000/docs 查看 API 文档
echo.
echo 按 Ctrl+C 停止服务
echo.

python main.py

pause
