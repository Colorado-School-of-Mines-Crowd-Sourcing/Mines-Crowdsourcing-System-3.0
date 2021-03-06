#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd minesCrowdsourcing; python manage.py createsuperuser --no-input)
fi
(cd minesCrowdsourcing; gunicorn minesCrowdsourcing.wsgi --user www-data --bind 0.0.0.0:9600 --workers 3) &
nginx -g "daemon off;"
