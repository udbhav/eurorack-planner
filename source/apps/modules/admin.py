from django.contrib import admin

from apps.modules.models import *

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'eurorackdb_id', 'manufacturer', 'updated', 'custom', 'current_12v', 'negative_current_12v', 'current_5v', 'msrp']
    list_filter = ['custom',]
    search_fields = ['name', 'manufacturer__name']

admin.site.register(Module, ModuleAdmin)
admin.site.register(Manufacturer)
admin.site.register(Setup)
