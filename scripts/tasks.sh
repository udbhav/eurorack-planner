#! /bin/bash    
#source /home/udbhav/www/django/eurorack-planner/env/bin/activate
export PYTHONPATH=/home/udbhav/www/django/eurorack-planner/app/source:$PYTHONPATH
#export DJANGO_SETTINGS_MODULE='settings'

/home/udbhav/www/django/eurorack-planner/env/bin/python /home/udbhav/www/django/eurorack-planner/app/scripts/update_data.py
/home/udbhav/www/django/eurorack-planner/env/bin/python /home/udbhav/www/django/eurorack-planner/app/source/manage.py update_index
