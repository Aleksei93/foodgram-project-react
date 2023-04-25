python manage.py collectstatic --noinput
python manage.py migrate
gunicorn foodgram.wsgi:application --bind 0:8000