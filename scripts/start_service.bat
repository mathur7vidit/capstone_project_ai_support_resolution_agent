@echo off

cd /d %~dp0..

call venv\Scripts\activate

start cmd /k "uvicorn app.main:app --reload"

timeout /t 5 >nul

start cmd /k "streamlit run ui/streamlit_app.py"

exit