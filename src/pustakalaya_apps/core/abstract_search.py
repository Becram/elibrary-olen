from elasticsearch_dsl import DocType, Date, Text, Keyword, Completion, Integer

class ItemDoc(DocType):
    """
    Common superclass for Document, Audio, Video, Wiki, Maps, and Newspaper.
    Don't get index in the index server."""
    id = Text()
    title = Text(fields={'keyword': Keyword()})
    title_suggest = Completion()
    abstract = Text(analyzer='snowball')
    type = Text(fields={'keyword': Keyword()})
    education_levels = Text(multi=True, fields={'keyword': Keyword()})
    communities = Text(analyzer='snowball',multi=True, fields={'keyword': Keyword()})
    collections = Text(multi=True, fields={'keyword': Keyword()})
    languages = Text(multi=True, fields={'keyword': Keyword()})
    description = Text(analyzer='snowball')
    license_type = Text(fields={'keyword': Keyword()})
    year_of_available = Date()
    publication_year = Date()
    created_date = Date()
    updated_date = Date()
    author_list = Keyword(fields={'keyword': Keyword()},multi=True)
    url = Text()
    view_count = Integer()
    published = Text(fields={'keyword': Keyword()})
