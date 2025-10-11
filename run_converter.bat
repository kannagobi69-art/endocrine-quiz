@echo off
title 🩺 GNM Quiz Converter - Auto Build Questions.js
color 0d
echo ==================================================
echo   School of Nursing - Endocrine Quiz Converter
echo   Prepared by K. Kannan
echo ==================================================
echo.

REM Navigate to the current folder (where this batch file is located)
cd /d "%~dp0"

REM Check for Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Python is not installed or not added to PATH.
    echo Please install Python 3.x from https://www.python.org/downloads/
    echo and make sure to check "Add to PATH" during installation.
    pause
    exit /b
)

echo --------------------------------------------------
echo Running Python converter to generate questions.js
echo --------------------------------------------------
python csv_to_questions.py

if errorlevel 1 (
    echo.
    echo ❌ Something went wrong while running the converter.
    echo Please check your mcqs.csv or Python installation.
    pause
    exit /b
)

echo.
echo ✅ Conversion complete! questions.js successfully updated.
echo --------------------------------------------------
echo.

REM Open folder and launch the quiz in browser
echo Opening project folder and launching quiz...
start "" "%~dp0index.html"
explorer "%~dp0"

echo.
echo You can close this window after verifying your quiz in the browser.
echo.
pause
