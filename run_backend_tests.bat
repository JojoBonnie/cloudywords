@echo off
echo Running backend tests...
cd backend
call .venv\Scripts\activate
python manage.py test