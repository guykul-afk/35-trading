@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Creating Python environment...
  py -m venv .venv || goto :error
)

echo Installing dashboard dependencies...
".venv\Scripts\python.exe" -m pip install -e . || goto :error

echo Starting TA-35 dashboard...
".venv\Scripts\python.exe" -m streamlit run app\Home.py
exit /b 0

:error
echo.
echo Setup failed. Make sure Python 3.11 or newer is installed.
pause
exit /b 1
