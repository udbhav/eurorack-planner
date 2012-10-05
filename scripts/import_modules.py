from django.core.management import setup_environ
from urllib import urlretrieve
from django.core.files import File

import json
import sys, os
sys.path.append("/Users/udbhav/Sites/eurorack-planner/source")

import settings

setup_environ(settings)

from apps.modules.models import Module, Manufacturer
try:
    json_string = open(sys.argv[1], "r")
except Exception as inst:
    print "please pass a valid filename with module json data to the script"
    print type(inst)
    print inst
else:
    modules = json.loads(json_string.read())
    for module in modules:
        manufacturer_name = module['manufacturer'].rstrip()
        try:
            manufacturer = Manufacturer.objects.get(name = manufacturer_name)
        except:
            manufacturer = Manufacturer.objects.create(name = manufacturer_name)
            manufacturer.save()

        for k,v in module.items():
            print k,v

            try:
                module[k] = v.rstrip()
            except:
                pass

            if not module[k] and (k == 'hp' or k == 'current_12v' or k == 'negative_current_12v' or k == 'current_5v' or k == 'depth'):
                module[k] = None
            elif not module[k]:
                module[k] = ''
            elif k == 'hp' or k == 'current_12v' or k == 'negative_current_12v' or k == 'current_5v' or k == 'depth':
                module[k] = int(float(module[k]))

        print module
        model_module = Module.objects.create(
            name = module['name'],
            manufacturer = manufacturer,
            hp = int(float(module['hp'])),
            depth = module['depth'],
            current_12v = module['current_12v'],
            negative_current_12v = module['negative_current_12v'],
            current_5v = module['current_5v'],
            msrp = module['msrp'].replace('$','').replace(',',''),
            url = module['url'],
            )

        try:
            image = module['image']
        except KeyError:
            image = None

        if image:
            outfolder = os.path.realpath(os.path.dirname(__file__))
            filename = image.split("/")[-1]
            outpath = os.path.join(outfolder, 'images', filename)

            if module['image'].lower().startswith("http"):
                urlretrieve(image, outpath)
            else:
                urlretrieve(urlparse.urlunparse(parsed), outpath)

            f = File(open(outpath, 'r'))
            model_module.image = f
            model_module.save()
