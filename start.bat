@echo off
cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║        🌍 ENGLISH LEARNING AI 🌍                         ║
echo ║        Chat • Voice • Learn • Progress                    ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

cd /d %~dp0

REM Activate venv
call venv\Scripts\activate.bat

REM Set API key
set GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE

REM Launch
echo.
echo Starting English Learning App on http://localhost:8501
echo.
python -m streamlit run voice_app.py

pause
