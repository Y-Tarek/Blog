#!/bin/sh
python manage.py migrate  --noinput
echo "database migrated"

echo "creating Superuser"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='Yasser').exists() or User.objects.create_superuser(email='yassertarek98@gmail.com',first_name='yasser',last_name='tarek',username='Yasser',password='123@123qb')" | python3 manage.py shell
echo "superuser created"

python manage.py collectstatic --noinput

chmod +x /app/staticfiles

gunicorn blog.wsgi -b 0.0.0.0:8001  --disable-redirect-access-to-syslog
