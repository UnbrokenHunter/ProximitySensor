@echo off
set VENV_DIR=.venv

:: Create venv if missing
if not exist %VENV_DIR% (
    python -m venv %VENV_DIR%
)

:: Activate venv
call %VENV_DIR%\Scripts\activate

:: Install dependencies if needed
pip install -r requirements/ requirements.txt

:: Run your script
python main.py
