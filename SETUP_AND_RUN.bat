@echo off
echo ========================================
echo  FCIT Backend - Automated Setup
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

echo [3/6] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [4/6] Running database migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migration failed
    pause
    exit /b 1
)
echo Database setup complete!
echo.

echo [5/6] Creating superuser...
echo.
echo Please enter superuser details:
echo NOTE: Email must end with @pucit.edu.pk
echo.
python manage.py createsuperuser
echo.

echo [6/6] Starting Django server...
echo.
echo ========================================
echo  Backend is ready!
echo ========================================
echo.
echo  API Documentation: http://localhost:8000/api/docs/
echo  Admin Panel:       http://localhost:8000/admin/
echo  API Root:          http://localhost:8000/api/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
