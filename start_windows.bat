@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv
  if errorlevel 1 goto failed
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
.venv\Scripts\python.exe setup_local.py
if errorlevel 1 goto failed
.venv\Scripts\python.exe manage.py migrate --noinput
if errorlevel 1 goto failed
echo Open http://127.0.0.1:8000 in your browser.
echo Local verification emails are saved in data\emails.
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
goto end
:failed
echo Startup failed. Read the error above. Python 3.12 or 3.13 is recommended.
pause
:end
endlocal
