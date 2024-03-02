@echo off
setlocal enabledelayedexpansion

REM Путь к Python
set "python_executable=python"
REM Имя виртуального окружения
set "venv_name=venv"
REM Путь к requirements.txt
set "requirements_file=requirements.txt"
REM Путь к файлу main.py
set "main_script=main.py"

REM Проверка существования виртуального окружения
if not exist %venv_name% (
    echo "Creating virtual environment..."
    %python_executable% -m venv %venv_name%
    call %venv_name%\Scripts\activate
    pip install -r %requirements_file%
)

REM Активация виртуального окружения
call %venv_name%\Scripts\activate

REM Запуск main.py
%python_executable% %main_script%

REM Деактивация виртуального окружения
deactivate

echo "Press any key to continue . . ."
pause
