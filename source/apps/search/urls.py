from django.conf.urls.defaults import *
from haystack.views import SearchView

urlpatterns = patterns(
    '',
    url(r'^$', SearchView(), name='haystack_search'),
    url(r'^autocomplete/$', 'apps.search.views.autocomplete', name='autocomplete'),
    )
