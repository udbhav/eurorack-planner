#! /bin/bash    
source /home/udbhav/www/django/eurorack-planner/env/bin/activate
export PYTHONPATH=/home/udbhav/www/django/eurorack-planner/app/source:$PYTHONPATH
python /home/udbhav/www/django/eurorack-planner/app/scripts/sync_data.py
