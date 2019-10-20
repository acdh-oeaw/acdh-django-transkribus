Readme
======

.. image:: https://badge.fury.io/py/acdh-django-transkribus.svg
    :target: https://badge.fury.io/py/acdh-django-transkribus

A django app for interacting with the [Transkribus-API](https://transkribus.eu/wiki/index.php/REST_Interface) to search and read documents hosted and processed by [Transkribus](https://transkribus.eu/Transkribus/)


Installation
------------

    pip install acdh-django-transkribus


Use:
------------

Add your user name and password and the ID of the collection you'd like to expose by the current application's settings file like shown below:


.. code-block:: python

    TRANSKRIBUS = {
        "user": "mytranskribususer@whatever.com",
        "pw": "mytranskribuspassword",
        "col_id": "43497"
    }


For custom translations you'd need to add following dict to your settings:


.. code-block:: python

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
            'result_link': 'go to document'
        },
        'page': {
            'img_col': 'IMG',
            'text_col': 'TEXT'
        },
        'docs': {
            'title_col': 'Title',
            'page_nr_col': 'Nr. of pages',
            'preview_col': 'Preview'
        }
    }
