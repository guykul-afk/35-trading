@echo off
title DDE Excel Auto-Exporter
:: Change directory to the batch file location (essential for scheduled task start path)
cd /d "%~dp0"
echo ===================================================
echo  DDE Live Sync - Excel Exporter Launcher
echo ===================================================
echo.
echo Starting Excel background synchronization...
echo Logs are being written to dde_sync.log
echo.
set PYTHONIOENCODING=utf-8
".\.venv\Scripts\python.exe" -u scripts\excel_auto_exporter.py > dde_sync.log 2>&1
