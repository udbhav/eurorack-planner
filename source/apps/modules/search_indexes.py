from haystack import indexes

from apps.modules.models import Module

class ModuleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name_auto = indexes.EdgeNgramField(model_attr='autocomplete_name')

    def get_model(self):
        return Module
