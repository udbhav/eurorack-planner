from django.views.generic import ListView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, BaseListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.db import models
from django import http
from django.utils import simplejson as json
from django.core import serializers
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from apps.modules.models import Manufacturer, Module

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        new_context = "{"
        i = 0

        for k,v in context.items():
            if v.__class__ == models.query.QuerySet:
                data = serializers.serialize("json", v, ensure_ascii=False)
            elif issubclass(v.__class__, models.Model):
                data = serializers.serialize("json", [v,], ensure_ascii=False)
            else:
                data = json.dumps(v)

            new_context += "\"%s\": %s" % (k, data)

            i += 1
            if i != len(context.items()):
                new_context += ", "

        new_context += "}"

        return new_context

class HybridListView(JSONResponseMixin, MultipleObjectTemplateResponseMixin, BaseListView):
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            return JSONResponseMixin.render_to_response(self, context)
        else:
            return MultipleObjectTemplateResponseMixin.render_to_response(self, context)

class HybridDetailView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            return JSONResponseMixin.render_to_response(self, context)
        else:
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)


class ManufacturersView(HybridListView):
    model = Manufacturer

class ModulesView(HybridListView):
    model = Module
    paginate_by = 50

class ModulesByManufacturer(ModulesView):

    def get_queryset(self):
        self.manufacturer = get_object_or_404(Manufacturer, pk=self.kwargs['pk'])
        return Module.objects.filter(manufacturer=self.manufacturer)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ModulesByManufacturer, self).get_context_data(**kwargs)
        context['manufacturer'] = self.manufacturer
        return context

class ModuleView(HybridDetailView):
    model = Module


def planner(request):
    manufacturers = Manufacturer.objects.all()
    modules = Module.objects.all()

    return render_to_response('modules/planner.html', {
            'manufacturers': manufacturers,
            'modules': modules,
    }, context_instance=RequestContext(request))

def save_to_file(request):
    if request.method == 'POST':
        preset = request.POST.get('preset', '')
        response = http.HttpResponse(preset, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="eurorack_setup.json"'
        return response
    else:
        return HttpReponse('')
