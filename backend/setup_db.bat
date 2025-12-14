@echo off
cd /d C:\Users\User\.gemini\antigravity\scratch\FCIT_PROJECT\backend
set PYTHONPATH=C:\Users\User\.gemini\antigravity\scratch\FCIT_PROJECT\backend
C:\Users\User\.gemini\antigravity\scratch\Talk-FCIT-Repo\.gemini\python\python.exe manage.py makemigrations
C:\Users\User\.gemini\antigravity\scratch\Talk-FCIT-Repo\.gemini\python\python.exe manage.py migrate
echo.
echo Migrations complete! Now creating superuser...
echo.
C:\Users\User\.gemini\antigravity\scratch\Talk-FCIT-Repo\.gemini\python\python.exe manage.py createsuperuser --email admin@pucit.edu.pk --noinput
pause
