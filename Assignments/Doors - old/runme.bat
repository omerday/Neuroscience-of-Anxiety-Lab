@setlocal enableextensions
@cd /d "%~dp0"
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)

if exist "C:\Program Files\PsychoPy3\python.exe" (
  echo Psychopy: Admin location installed
  "C:\Program Files\PsychoPy3\python.exe" main.py
) 

if exist "C:\Program Files\PsychoPy\python.exe" (
  echo Psychopy: Admin location installed
  "C:\Program Files\PsychoPy\python.exe" main.py
) 
