from django.conf.urls.defaults import patterns, url

from apps.modules.views import ManufacturersView, ModulesByManufacturer, ModuleView, ModulesView, JSONModuleView

urlpatterns = patterns(
    '',
    url(r'^manufacturers/$', ManufacturersView.as_view(), {}, name='manufacturers'),
    url(r'^manufacturers/(?P<pk>\d+)/modules/$', ModulesByManufacturer.as_view(), name='modules_by_manufacturer'),
    url(r'^$', ModulesView.as_view(), {}, name='modules'),
    url(r'^(?P<pk>\d+)/$', ModuleView.as_view(), name='module'),
    url(r'^json/(?P<pk>\d+)/$', JSONModuleView.as_view(), name='json_module'),
    url(r'^planner/$', 'apps.modules.views.planner',  name='planner'),
    url(r'^save-to-file/$', 'apps.modules.views.save_to_file', name='save_to_file'),
)
