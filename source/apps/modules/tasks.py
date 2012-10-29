import json, urllib, StringIO

from celery import task
from PIL import Image
from django.conf import settings
from django.core.mail import EmailMessage

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
