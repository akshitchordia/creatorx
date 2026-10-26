@echo off
title Creator Finder - local server
cd /d "%~dp0"
set PORT=8080
echo.
echo  Creator Finder is starting at http://localhost:%PORT%
echo  Keep this window open while you use the site. Close it to stop.
echo.
start "" cmd /c "timeout /t 2 >nul & start http://localhost:%PORT%"
where py >nul 2>nul && (py -m http.server %PORT% & goto :end)
python --version >nul 2>nul && (python -m http.server %PORT% & goto :end)
where npx >nul 2>nul && (npx --yes serve -l %PORT% . & goto :end)
echo.
echo  Python or Node.js is needed to run the local server.
echo  Install Python from https://www.python.org/downloads/ (tick "Add python.exe to PATH"),
echo  then double-click this file again.
:end
pause
