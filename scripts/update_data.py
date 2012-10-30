from django.core.management import setup_environ
import settings

setup_environ(settings)

from apps.modules.tasks import update_data
update_data.delay()



        

