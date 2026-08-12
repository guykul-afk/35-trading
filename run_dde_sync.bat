@echo off
title DDE Excel Auto-Exporter
echo ===================================================
echo  DDE Live Sync - Excel Exporter Launcher
echo ===================================================
echo.
echo Starting Excel background synchronization...
echo.
".\.venv\Scripts\python.exe" scripts\excel_auto_exporter.py
pause
