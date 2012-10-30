from django.core.management import setup_environ
import settings

setup_environ(settings)




# import/update modules from eurorackdb.com
def import_modules():
    from apps.modules.importers import EurorackDBImporter
    importer = EurorackDBImporter()
    importer.sync_data()

# save images if necessary

