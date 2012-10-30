import json, urllib, StringIO
from itertools import chain
from datetime import datetime, timedelta

from celery import task
from PIL import Image
from django.conf import settings
from django.core.mail import EmailMessage

from apps.modules.importers import EurorackDBImporter
from apps.modules.models import Module

@task()
def build_setup_image(json_string, email):
    row_height = 262
    hp_unit = 10

    data = json.loads(json_string)

    # Calculate canvas size
    hp_width = 0
    for row in data['rows']:
        if int(row['size']) > hp_width:
            hp_width = int(row['size'])

    width = hp_width * hp_unit
    height = len(data['rows']) * row_height

    image = Image.new("RGB", [width, height])

    # build each row
    i = 0
    row_image = Image.open(open(settings.STATIC_ROOT + '/images/euro_rails.png'))
    for row in data['rows']:
        # add screw holes
        ri = 0
        while ri < int(row['size']):
            image.paste(row_image, (ri * hp_unit, i * row_height))
            ri += 1

        # add modules
        for module in row['modules']:
            try:
                module_image = Image.open(urllib.urlretrieve(module['image'])[0])
            except:
                module_image = None

            if module_image:
                module_image = module_image.resize( (hp_unit * int(module['size']), row_height), Image.ANTIALIAS )
                x = int(module['left'].replace('px', ''))
                image.paste(module_image, (x, i * row_height))

        i += 1


    image_string = StringIO.StringIO()
    image.save(image_string, format="JPEG")
    email = EmailMessage('Your image from eurorackplanner.com', 'Happy wiggling!', settings.DEFAULT_FROM_EMAIL, [email,])
    email.attach('eurorack_setup.jpg',image_string.getvalue(),'image/jpeg')
    email.send(fail_silently=False)

@task()
def update_data():
    # first let's update the module data from eurorackdb.com
    importer = EurorackDBImporter()
    importer.sync_data()

    # then we deal with the images
    # let's handle modules with no images first, these would be the new ones
    new_modules = Module.objects.filter(image='').exclude(eurorackdb_image='')

    # now modules that have been updated within the last 6 hours, maybe the image has changed.
    updated_modules = Module.objects.exclude(eurorackdb_image='').filter(updated__gte=datetime.now() - timedelta(hours=6))

    # combine the two querysets
    modules = chain(new_modules, updated_modules)

    # make it unique
    modules = list(set(modules))

    for module in modules:
        module.save_eurorackdb_image()

    
