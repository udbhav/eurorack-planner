================
Eurorack Planner
================

http://eurorackplanner.com

Eurorack Planner is a Django project to help modular synthesis addicts plan the best way to spend all of their discretionary income.

Setup
-----

* Use pip to install the requirements::

    pip install requirements.txt

* Create /source/settings/local.py (see /source/settings/local.example.py)

* Sync your databases::

    python manage.py syncdb
    python manage.py migrate

* Start your server::

  python manage.py runserver


