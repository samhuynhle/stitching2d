@echo off
title Stitching2D Local CAD Server (:5050)
cd /d "%~dp0"
echo ===================================================
echo   Stitching2D CAD & Sewing Planner Server
echo   Running at http://localhost:5050
echo ===================================================
..\.venv\Scripts\python.exe -m uvicorn src.server:app --host 0.0.0.0 --port 5050 --reload
pause
