from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'apps.modules.views.planner'),
    url(r'^modules/', include('apps.modules.urls')),
    url(r'^search/', include('apps.search.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
)

if getattr(settings, 'LOCAL_SERVE', False):
    urlpatterns = patterns('django.views.static',
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'), 'serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ) + staticfiles_urlpatterns() + urlpatterns
