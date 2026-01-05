@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   SubtitleToolbox Auto Build Script
echo ============================================

if not exist "SubtitleToolbox.py" (
    echo [Error] SubtitleToolbox.py not found!
    pause
    exit
)

python -m PyInstaller SubtitleToolbox.spec --distpath="." --workpath="C:/Temp_Build" --clean

echo.
echo --------------------------------------------
echo Build completed!
echo --windowed mode enabled.
echo Output directory: Current directory
echo --------------------------------------------
pause