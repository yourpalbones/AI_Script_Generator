@echo off
echo Starting ScriptWriter...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo Error starting ScriptWriter.
    echo Please check that Python is installed and all dependencies are available.
    echo.
    pause
)
