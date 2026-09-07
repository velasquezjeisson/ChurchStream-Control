@echo off
title ChurchStream Control
cd /d "%~dp0"
set "OPENLP_EXE="
if exist "%ProgramFiles%\OpenLP\OpenLP.exe" set "OPENLP_EXE=%ProgramFiles%\OpenLP\OpenLP.exe"
if not defined OPENLP_EXE if exist "%ProgramFiles(x86)%\OpenLP\OpenLP.exe" set "OPENLP_EXE=%ProgramFiles(x86)%\OpenLP\OpenLP.exe"
if not defined OPENLP_EXE if exist "%LocalAppData%\Programs\OpenLP\OpenLP.exe" set "OPENLP_EXE=%LocalAppData%\Programs\OpenLP\OpenLP.exe"
tasklist /FI "IMAGENAME eq OpenLP.exe" 2>NUL | find /I "OpenLP.exe" >NUL
if errorlevel 1 if defined OPENLP_EXE start "" /min "%OPENLP_EXE%"
if errorlevel 1 timeout /t 5 /nobreak >nul
start "" http://127.0.0.1:8765/
where py >nul 2>nul && py servidor.py || python server.py
