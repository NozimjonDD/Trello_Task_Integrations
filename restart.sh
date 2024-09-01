#!/usr/bin/env bash


pip install -r requirements.txt

python manage.py collectstatic --noinput


python manage.py migrate

sudo systemctl restart gunicorn.service
sudo systemctl restart gunicorn.service

echo -e "\033[1m Restarted! \033[0m"

