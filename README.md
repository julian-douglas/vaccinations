# Vaccinations Django App

## Setup
1. Create virtualenv (optional) and install dependencies:
```
pip install -r requirements.txt
```
2. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```
3. Create superuser:
```
python manage.py createsuperuser
```
4. Seed data:
```
python manage.py seed_data
```
5. Run server:
```
python manage.py runserver
```
6. Visit http://127.0.0.1:8000/

Login via /admin or /accounts/login/.

## Features
- Manage vaccines, branches, appointments, doses via admin.
- User login/logout.
- Create, edit, delete appointments from UI.
