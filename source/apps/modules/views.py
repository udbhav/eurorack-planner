from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, BaseListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.db import models
from django import http
from django.utils import simplejson as json
from django.core import serializers
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from apps.modules.models import Manufacturer, Module, Setup
from apps.modules.forms import CustomModuleForm, SetupForm

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

class ManufacturersView(ListView):
    model = Manufacturer

class ModulesView(ListView):
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

class ModuleView(DetailView):
    model = Module

class JSONModuleView(JSONResponseMixin, BaseDetailView):
    model = Module
    context_object_name = 'module'
    
    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        module = get_object_or_404(Module, pk=pk)
        module_object = {
            'id': module.id,
            'name': module.name,
            'image': module.get_display_image_url(),
            'hp': module.hp,
            'depth': module.depth,
            'current_12v': module.current_12v,
            'negative_current_12v': module.negative_current_12v,
            'msrp': str(module.msrp),
            'planner_url': module.get_absolute_url(),
            'url': module.url,
            'current_5v': module.current_5v,
            }

        if module.manufacturer:
            module_object['manufacturer'] = module.manufacturer.name
            module_object['manufacturer_id'] = module.manufacturer.id
        else:
            module_object['manufacturer'] = None
            module_object['manufacturer_id'] = None

        return module_object

class CustomModulesView(ListView):
    model = Module
    template_name = "modules/custom_module_list.html"

    def get_queryset(self):
        return Module.objects.filter(user=self.request.user)

class NewCustomModuleView(CreateView):
    model = Module
    form_class = CustomModuleForm
    success_url = '/modules/custom/'

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['instance'] = Module(custom=True, user=self.request.user)
        return CustomModuleForm(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewCustomModuleView, self).get_context_data(**kwargs)
        context['create'] = True
        return context

class EditCustomModuleView(UpdateView):
    model = Module
    form_class = CustomModuleForm
    success_url = '/modules/custom/'

    def form_valid(self, form):
        module = form.save(commit=False)
        if module.user == self.request.user:
            self.object = form.save()
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return http.HttpResponseForbidden()

class DeleteCustomModuleView(DeleteView):
    model = Module
    success_url = '/modules/custom/'
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return http.HttpResponseForbidden()
        else:
            self.object.delete()
            return http.HttpResponseRedirect(self.get_success_url())

class SetupsView(JSONResponseMixin, BaseListView):
    model = Setup

    def get_queryset(self):
        return Setup.objects.filter(user=self.request.user)

class SetupView(JSONResponseMixin, BaseDetailView):
    model = Setup
    context_object_name = 'setup'
    
def planner(request):
    if request.user.is_authenticated():
        custom_modules = Module.objects.filter(user=request.user)
        saved_setups = Setup.objects.filter(user=request.user)
    else:
        custom_modules = []
        saved_setups = []

    return render_to_response('modules/planner.html', {
            'custom_modules': custom_modules,
            'saved_setups': saved_setups,
    }, context_instance=RequestContext(request))

def save_to_file(request):
    if request.method == 'POST':
        preset = request.POST.get('preset', '')
        response = http.HttpResponse(preset, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="eurorack_setup.json"'
        return response
    else:
        return http.HttpReponse('')

def save_setup(request):
    if request.method == 'POST' and request.user.is_authenticated():
        setup = Setup(user = request.user)
        form = SetupForm(request.POST, instance=setup)
        if form.is_valid():
            setup = form.save()
            return http.HttpResponse(setup.id)
        else:
            assert False
            return http.HttpResponse('did not save')            
    else:
        return http.HttpResponse('did not save')

@login_required
def delete_setup(request, pk):
    setup = get_object_or_404(Setup, pk=pk)
    if request.method == 'POST' and setup.user == request.user:
        setup.delete()
        return http.HttpResponse('Deleted')
    else:
        return http.HttpResponseForbidden()
