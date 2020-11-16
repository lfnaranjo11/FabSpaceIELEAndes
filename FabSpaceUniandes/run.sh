cd FabSpaceRestApi
python manage.py makemigrations api
python manage.py migrate
gunicorn --workers=5 --bind 0.0.0.0:8000 -m 007 FabSpaceRestApi.wsgi:application