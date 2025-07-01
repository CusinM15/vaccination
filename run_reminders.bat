@echo off
call C:\Matej\GitHub\vaccination\venv\Scripts\activate.bat
cd /d C:\Matej\GitHub\vaccination

python manage.py send_reminders 

