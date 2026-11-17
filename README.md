# WanderWorld
A beginner-friendly Django travel social network.

## Features
- Sign up, log in and log out
- Create travel posts with optional photos and locations
- Home feed with newest posts first
- Like/unlike posts
- Add comments
- Follow/unfollow other travellers
- Search travellers and destinations
- Edit your profile (bio, location and profile photo)
- Django admin

## Run on Windows (VS Code / PowerShell)
Open the `WanderWorld` folder in VS Code. In the terminal:

```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations social
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

If PowerShell says script execution is disabled, run the `Set-ExecutionPolicy` command above in that same terminal, then activate again.

## Project structure
- `config/` - Django project settings and root URLs
- `social/` - app models, views, forms and URLs
- `social/templates/social/` - HTML templates
- `static/` - CSS
- `media/` - uploaded images (created automatically)

This is a learning/demo project. Before public deployment, configure production security settings, static file hosting, and a production database.
