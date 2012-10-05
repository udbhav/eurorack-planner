import json
from django.http import HttpResponse
from haystack.query import SearchQuerySet

def autocomplete(request):
    results = SearchQuerySet().autocomplete(name_auto=request.GET.get('term', ''))[:10]
    return_results = []
    for result in results:
        return_results.append({'label': result.name_auto, 'id': result.pk})
    
    return HttpResponse(json.dumps(return_results), content_type='application/json')
