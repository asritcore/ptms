@echo off
:: ── PTMS Start Script (Windows) ───────────────────────────────────
:: Double-click this every day to start the application
:: ──────────────────────────────────────────────────────────────────

echo.
echo   Starting PTMS Backend...
echo   Local  : http://localhost:8000
echo   Live   : https://ptms.apptms.org
echo.
echo   Keep this window open while the app is running.
echo   Press Ctrl+C to stop.
echo.

cd /d "%~dp0backend"

:: Check venv exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] venv not found. Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
