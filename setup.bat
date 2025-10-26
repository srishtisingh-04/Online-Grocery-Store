@echo off
REM Online Grocery Store - Windows Setup Script

echo 🛒 Online Grocery Store Setup
echo ==============================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ pip found

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Python dependencies installed successfully

REM Check if MySQL is installed
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  MySQL is not installed. Please install MySQL 5.7+ first.
    echo    You can download it from: https://dev.mysql.com/downloads/
    pause
    exit /b 1
)

echo ✅ MySQL found

REM Create database
echo 🗄️  Setting up database...
echo Please enter your MySQL root password:
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS grocery_store;"

if %errorlevel% neq 0 (
    echo ❌ Failed to create database
    pause
    exit /b 1
)

echo ✅ Database created successfully

REM Import database schema
echo 📋 Importing database schema...
mysql -u root -p grocery_store < database/schema.sql

if %errorlevel% neq 0 (
    echo ❌ Failed to import database schema
    pause
    exit /b 1
)

echo ✅ Database schema imported successfully

REM Import initial data
echo 📊 Importing initial data...
mysql -u root -p grocery_store < database/init_data.sql

if %errorlevel% neq 0 (
    echo ❌ Failed to import initial data
    pause
    exit /b 1
)

echo ✅ Initial data imported successfully

REM Create .env file
echo ⚙️  Creating environment configuration...
if not exist .env (
    copy env.example .env
    echo ✅ Environment file created (.env)
    echo ⚠️  Please update the .env file with your database credentials
) else (
    echo ✅ Environment file already exists
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. Update the .env file with your database credentials
echo 2. Run the application: python app.py
echo 3. Open your browser and go to: http://localhost:5000
echo.
echo Default login credentials:
echo Admin: username=admin, password=admin123
echo Customer: username=customer1, password=customer123
pause
