import requests
import json
import pprint

from django.core.exceptions import ObjectDoesNotExist

from apps.modules.models import Module, Manufacturer

class EurorackDBImporter(object):
    modules = None
    fields = [
        ['eurorackdb_id', 'module_id'],
        ['name', 'module_name'],
        ['eurorackdb_image', 'module_image_file'],
        ['hp', 'module_width_hp'],
        ['current_12v', 'module_current_plus_12v_ma'],
        ['negative_current_12v', 'module_current_neg_12v_ma'],
        ['current_5v', 'module_current_plus_5v_ma'],
        ['url', 'module_url'],
        ['msrp', 'module_msrp'],
        ]
    string_fields = ['name', 'eurorackdb_image', 'url']

    def get_local_data(self, filepath):
        f = open(filepath, 'r')
        self.modules = json.loads(f.read())['results']

    def get_remote_data(self):
        response = requests.get("http://eurorackdb.com/node/h_eurorack_planner_feed")
        self.modules = json.loads(response.text)['results']

    def create_module(self, m):
        try:
            manufacturer = Manufacturer.objects.get(name=m['mfr_name'])
        except ObjectDoesNotExist:
            manufacturer = Manufacturer.objects.create(name=m['mfr_name'])

        new_module = Module(manufacturer=manufacturer)

        for field in self.fields:
            setattr(new_module, field[0], m[field[1]])

        new_module.save()

    def update_module(self, current_module, new_module):
        update = False

        for field in self.fields:
            # We need to make sure types are correct before we compare
            old_value = getattr(current_module, field[0])
            if old_value:
                old_value = str(old_value)
            elif field[0] in self.string_fields:
                old_value = ''
            else:
                # values could be 0, 0.00, or None
                if old_value is not None:
                    old_value = str(old_value)

            if old_value != new_module[field[1]]:
                print 'something changed\n'
                print field
                print old_value
                print new_module[field[1]]
                update = True

        if update:
            pprint.pprint(new_module)
            print 'updating\n'
            for field in self.fields:
                setattr(current_module, field[0], new_module[field[1]])

            current_module.save()

    def prepare_data(self, json_module):
        for field in self.fields:
            # handle msrp dollar signs
            if field[0] == 'msrp':
                json_module[field[1]] = json_module[field[1]].replace('$','').replace(',','').replace('.00','')

            # Strings must not be None type
            if json_module[field[1]] == None and field[0] in self.string_fields:
                json_module[field[1]] = ''

        return json_module

    def sync_data(self):
        if not self.modules:
            self.get_remote_data()

        for m in self.modules:
            # prepare the data
            m = self.prepare_data(m)

            # see if we have the module already
            try:
                current_module = Module.objects.get(eurorackdb_id=m['module_id'])
            except ObjectDoesNotExist:
                print 'creating\n'
                pprint.pprint(m)
                print '\r'

                self.create_module(m)
            else:
                self.update_module(current_module, m)
