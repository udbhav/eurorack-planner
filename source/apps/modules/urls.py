from django.conf.urls.defaults import patterns, url

from apps.modules.views import ManufacturersView

urlpatterns = patterns(
    'apps.modules.views',
    url(r'^manufacturers/$', ManufacturersView.as_view(), name='manufacturers')
)
