from haystack import indexes, site

from apps.modules.models import Module

class ModuleIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name_auto = indexes.EdgeNgramField(model_attr='autocomplete_name')

    def get_model(self):
        return Module

    def index_queryset(self):
        return Module.objects.all()

site.register(Module, ModuleIndex)
