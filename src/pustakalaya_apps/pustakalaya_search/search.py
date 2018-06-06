from django.conf import settings
from pustakalaya_apps.audio.search import AudioDoc
from pustakalaya_apps.video.search import VideoDoc
from pustakalaya_apps.document.search import DocumentDoc
from elasticsearch_dsl import (
    FacetedSearch,
    TermsFacet,
    DateHistogramFacet,
    SF,
    Q
)


class PustakalayaSearch(FacetedSearch):


    def __init__(self, search_types, sort_values, *args, **kwargs):
        # Doc types to search
        self.doc_types = search_types
        self.sort_values = sort_values
        self.filter_values = kwargs.get('filters')
        super(PustakalayaSearch, self).__init__(*args, **kwargs)

    index = settings.ES_INDEX
    # Boost values
    fields = [
        'title^10',
        'keywords',
        'abstract^5',
        'description',
        'collections',
        'communities',
        'author_list',
        'education_levels',
        'publisher',
        'license_type',
        'languages',
        'type',

    ]

    # Note: size =1000 means we are showing maximum 1000 items
    # this can cause problem if the value exceeds 1000 items
    facets = {
        'type': TermsFacet(field='type.keyword', size=1000),
        'languages': TermsFacet(field='languages.keyword', size=1000),
        'education_levels': TermsFacet(field='education_levels.keyword', size=1000),
        'communities': TermsFacet(field='communities.keyword', size=1000),
        'collections': TermsFacet(field='collections.keyword', size=10000),
        'keywords': TermsFacet(field='keywords.keyword', size=10000),
        'year_of_available': DateHistogramFacet(field='year_of_available', interval='month', min_doc_count=0),
        'license_type': TermsFacet(field='license_type.keyword', size=1000),
        'publication_year': DateHistogramFacet(field='year_of_available', interval='month', min_doc_count=0),
    }

    def search(self):
        # override methods to add custom pieces
        s = super(PustakalayaSearch,self).search().query("match", published="yes")
        s.filter(**self.filter_values)
        # s.sort({'title.keyword': {"order": "asc"}})
        return s


    # def sort(self, search):
    #     return self.search().sort(*self.sort_values)
