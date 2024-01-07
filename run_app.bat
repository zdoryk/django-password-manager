@echo off

:: Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate

:: Get the current directory path
set "currentDirectory=%CD%"

:: Construct the full path to the manage.py script
set "managePyPath=%currentDirectory%\manage.py"

:: Install pypoetry
python -m pip install poetry

:: Create poetry.lock and install dependencies
poetry lock
poetry install

:: Run the Django development server
@REM python "%managePyPath%" runserver
python "password_manager\manage.py" makemigrations
python "password_manager\manage.py" migrate

:: Open localhost:8080 in the default web browser
start http://localhost:8000
python "password_manager\manage.py" runserver

:: Pause to keep the command prompt window open
pause
