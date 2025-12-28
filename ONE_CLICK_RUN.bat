@echo off
TITLE FCIT App Starter

echo ===================================================
echo      Starting Talk@FCIT Application
echo ===================================================
echo.

:: 1. Start Database (Docker)
echo [1/3] Starting Database (Docker)...
docker-compose up -d db
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Docker is not running or failed to start!
    echo Please make sure Docker Desktop is open.
    pause
    exit /b
)
echo Database started successfully.
echo.

:: 2. Start Backend
echo [2/3] Starting Backend Server...
cd backend
:: Install dependency just in case
C:\Users\User\.gemini\antigravity\scratch\Talk-FCIT-Repo\.gemini\python\python.exe -m pip install dj-database-url > nul
::  Start Server in new window
start "Talk@FCIT Backend" cmd /k "C:\Users\User\.gemini\antigravity\scratch\Talk-FCIT-Repo\.gemini\python\python.exe manage.py runserver"
cd ..
echo Backend server launching in new window...
echo.

:: 3. Start Frontend
echo [3/3] Starting Frontend...
cd frontend
start "Talk@FCIT Frontend" cmd /k "npm run dev"
cd ..
echo Frontend server launching in new window...

echo.
echo ===================================================
echo      All systems go!
echo      Frontend: http://localhost:5173
echo      Backend:  http://localhost:8000
echo ===================================================
echo.
pause
