@echo off
title Stitching2D Local CAD Server (:5055)
cd /d "%~dp0"
echo ===================================================
echo   Stitching2D CAD & Sewing Planner Server
echo   Running at http://localhost:5055
echo ===================================================
echo Starting Stitching2D on http://localhost:5055 ...
python -m uvicorn src.server:app --host 0.0.0.0 --port 5055 --reload
pause
