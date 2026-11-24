@echo off
cd /d "%~dp0"
if exist "%USERPROFILE%\.conda\envs\juanzhi\python.exe" (
  "%USERPROFILE%\.conda\envs\juanzhi\python.exe" app.py --browser
) else (
  python app.py --browser
)
if errorlevel 1 pause
