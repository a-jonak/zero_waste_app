web: gunicorn food_management.wsgi:application --log-file - --log-level debug
python food_management/manage.py collectstatic --noinput
python food_management/manage.py makemigrations
python food_management/manage.py migrate
python food_management/manage.py runserver
