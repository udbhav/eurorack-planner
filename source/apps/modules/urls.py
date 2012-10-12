from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from apps.modules.views import *

urlpatterns = patterns(
    '',
    url(r'^manufacturers/$', ManufacturersView.as_view(), {}, name='manufacturers'),
    url(r'^manufacturers/(?P<pk>\d+)/modules/$', ModulesByManufacturer.as_view(), name='modules_by_manufacturer'),
    url(r'^$', ModulesView.as_view(), {}, name='modules'),
    url(r'^(?P<pk>\d+)/$', ModuleView.as_view(), name='module'),
    url(r'^json/(?P<pk>\d+)/$', JSONModuleView.as_view(), name='json_module'),
    url(r'^planner/$', 'apps.modules.views.planner',  name='planner'),
    url(r'^save-to-file/$', 'apps.modules.views.save_to_file', name='save_to_file'),
    url(r'^custom/$', login_required(CustomModulesView.as_view()), name='custom_modules'),
    url(r'^custom/new$', login_required(NewCustomModuleView.as_view()), name='new_custom_module'),
    url(r'^custom/(?P<pk>\d+)/$', login_required(EditCustomModuleView.as_view()), name='edit_custom_module'),
    url(r'^custom/(?P<pk>\d+)/delete/$', login_required(DeleteCustomModuleView.as_view()), name='delete_custom_module'),
)
