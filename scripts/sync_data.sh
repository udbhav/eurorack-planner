#! /bin/bash    
source /home/udbhav/www/django/eurorack-planner/env/bin/activate
PATH=/home/udbhav/www/django/eurorack-planner/app/source:$PATH
DJANGO_SETTINGS_MODULE='settings'
python sync_data.py
