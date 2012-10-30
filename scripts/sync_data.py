from django.core.management import setup_environ
import settings

setup_environ(settings)

from apps.modules.importers import EurorackDBImporter

importer = EurorackDBImporter()
importer.sync_data()
