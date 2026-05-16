@echo off
REM NSE Automation Application Launcher
REM This batch file makes it easy to run the automation on Windows

cd /d C:\Users\Prakhar\Desktop\AICode

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import selenium, pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run the application
echo.
echo Starting NSE Automation Application...
echo.
echo Options:
echo   1. Run once (test mode)
echo   2. Run continuously (every 2 minutes)
echo   3. Run with custom interval
echo   4. Run in debug mode (show browser)
echo   5. Exit
echo.

set /p choice="Choose option (1-5): "

if "%choice%"=="1" (
    python nse_automation_app.py --run-once
) else if "%choice%"=="2" (
    python nse_automation_app.py
) else if "%choice%"=="3" (
    set /p interval="Enter interval in seconds (default 120): "
    if "%interval%"=="" set interval=120
    python nse_automation_app.py --interval %interval%
) else if "%choice%"=="4" (
    python nse_automation_app.py --run-once --no-headless
) else if "%choice%"=="5" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice
    pause
    exit /b 1
)

pause
