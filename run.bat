@echo off
title SlideGen AI - Free Student PPT Maker
echo ========================================================
echo   SlideGen AI - Free AI Presentation Maker for Students
echo ========================================================
echo.
echo [1/2] Checking Python requirements...
python -m pip install -r requirements.txt --quiet
echo [2/2] Launching SlideGen Web Server...
echo.
echo --------------------------------------------------------
echo  SlideGen is starting at: http://127.0.0.1:8000
echo  Press Ctrl+C to stop the server anytime.
echo --------------------------------------------------------
echo.
start http://127.0.0.1:8000
python main.py
pause
