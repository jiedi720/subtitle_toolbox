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

python -m PyInstaller --noconfirm --onefile --windowed --name="SubtitleToolbox" --collect-all "send2trash" --icon="resources\SubtitleToolbox.ico" --add-data "logic;logic" --add-data "control;control" --add-data "function;function" --add-data "gui;gui" --add-data "font;font" --add-data "config;config" --add-data "resources\SubtitleToolbox.ico;." --hidden-import="reportlab" --hidden-import="reportlab.platypus" --hidden-import="reportlab.lib.styles" --hidden-import="pysrt" --hidden-import="pysubs2" --hidden-import="docx" --hidden-import="pypdf" --hidden-import="send2trash" --distpath="." --workpath="C:/Temp_Build" --clean SubtitleToolbox.py

echo.
echo --------------------------------------------
echo Build completed!
echo --windowed mode enabled.
echo Output directory: Current directory
echo --------------------------------------------
pause