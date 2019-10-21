from django.conf import settings

TRANSKRIBUS_TRANSLATIONS_DEFAULT = {
    'search_form': {
        'prefil': 'search in all documents',
        'button': 'Go!'
    },
    'search_header': {
        'header': 'Fulltext Search'
    },
    'hits': {
        'facet_header': 'refine your search',
        'facet_doc_title': 'Document',
        'result_header': 'Results',
        'kwic_header': 'KWIC',
        'result_col': 'Collection',
        'result_doc': 'Document',
        'result_page': 'Page',
        'result_link': 'go to document',
        'hits': 'hits',
        'prev': 'prev',
        'next': 'next'
    },
    'page': {
        'img_col': 'IMG',
        'text_col': 'TEXT'
    },
    'docs': {
        'title_col': 'Title',
        'page_nr_col': 'Nr. of pages',
        'preview_col': 'Preview',
        'doc_singular': 'Document',
        'doc_plural': 'Documents',
        'page_singular': 'Page',
        'page_plural': 'Pages'
    }
}


try:
    TRANSKRIBUS_TRANSLATIONS = settings.TRANSKRIBUS_TRANSLATIONS
except AttributeError:
    TRANSKRIBUS_TRANSLATIONS = TRANSKRIBUS_TRANSLATIONS_DEFAULT
