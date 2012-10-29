from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from apps.modules.views import *

urlpatterns = patterns(
    '',
    #url(r'^manufacturers/$', ManufacturersView.as_view(), {}, name='manufacturers'),
    #url(r'^manufacturers/(?P<pk>\d+)/modules/$', ModulesByManufacturer.as_view(), name='modules_by_manufacturer'),

    url(r'^$', ModulesView.as_view(), {}, name='modules'),
    url(r'^(?P<pk>\d+)/$', ModuleView.as_view(), name='module'),
    url(r'^json/(?P<pk>\d+)/$', JSONModuleView.as_view(), name='json_module'),

    url(r'^setups/$', login_required(SetupsView.as_view()), name='setups'),
    url(r'^setup/(?P<pk>\d+)/$', login_required(SetupView.as_view()), name='setup'),
    url(r'^setup/(?P<pk>\d+)/delete/$', 'apps.modules.views.delete_setup', name='delete_setup'),

    url(r'^setup/save/$', 'apps.modules.views.save_setup', name='save_online_setup'),
    
    url(r'^planner/$', 'apps.modules.views.planner',  name='planner'),
    url(r'^save-to-file/$', 'apps.modules.views.save_to_file', name='save_to_file'),

    url(r'^save-setup-image/$', 'apps.modules.views.save_setup_image', name='save_setup_image'),

    url(r'^custom/$', login_required(CustomModulesView.as_view()), name='custom_modules'),
    url(r'^custom/new$', login_required(NewCustomModuleView.as_view()), name='new_custom_module'),
    url(r'^custom/(?P<pk>\d+)/$', login_required(EditCustomModuleView.as_view()), name='edit_custom_module'),
    url(r'^custom/(?P<pk>\d+)/delete/$', login_required(DeleteCustomModuleView.as_view()), name='delete_custom_module'),
)
