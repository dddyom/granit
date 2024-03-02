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
    echo "Создание виртуального окружения..."
    %python_executable% -m venv %venv_name%
)

REM Активация виртуального окружения
call %venv_name%\Scripts\activate

REM Проверка установленных библиотек
set "installed_libs="
for /f "delims=" %%i in ('pip freeze ^| find /i /v "pkg-resources"') do (
    set "installed_libs=!installed_libs! %%i"
)

REM Установка библиотек из requirements.txt, если их нет
for /f "delims=" %%i in (%requirements_file%) do (
    echo !installed_libs! | find /i "%%i" >nul || pip install %%i
)

REM Запуск main.py
%python_executable% %main_script%

REM Деактивация виртуального окружения
deactivate

echo "Скрипт завершен."
