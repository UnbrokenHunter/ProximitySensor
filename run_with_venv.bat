@echo off
setlocal
set VENV_DIR=.venv

:: Create venv if missing
if not exist %VENV_DIR% (
    echo [INFO] Creating virtual environment...
    python -m venv %VENV_DIR%
)

:: Activate venv
call %VENV_DIR%\Scripts\activate

:: Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo [INFO] Installing main requirements...
pip install -r requirements\requirements.txt

echo [INFO] Installing PyTorch-specific requirements...
pip install -r requirements\pytorch.txt

:: Run your script
echo [INFO] Running main script...
python scripts\main.py

endlocal
