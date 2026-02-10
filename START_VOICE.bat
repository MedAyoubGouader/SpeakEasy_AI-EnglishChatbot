@echo off
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        🎤 ENGLISH LEARNING AI - VOICE MODE 🎤                ║
echo ║        Speak • Listen • Learn • Improve                      ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d %~dp0

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Set API key
set GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE

REM Launch Voice App
python -m streamlit run voice_app.py
echo.
echo Starting English Voice Learning App...
echo.
echo ┌────────────────────────────────────────────────────────────┐
echo │  Open your browser at: http://localhost:8506               │
echo │                                                            │
echo │  Features:                                                 │
echo │  🎤 Click microphone to speak                              │
echo │  🔊 Auto-play AI responses                                 │
echo │  ✏️ Grammar correction                                     │
echo │  📊 Multiple English levels                                │
echo └────────────────────────────────────────────────────────────┘
echo.

python -m streamlit run voice_app.py --server.port 8506

pause
