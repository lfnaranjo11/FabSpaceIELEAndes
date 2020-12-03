cd FabSpaceRestApi
python manage.py makemigrations api
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 FabSpaceRestApi.wsgi:application