from django.views.generic import ListView

from apps.modules.models import Manufacturer

class ManufacturersView(ListView):
    model = Manufacturer
