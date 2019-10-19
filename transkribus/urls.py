from django.conf.urls import url
from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'transkribus'


urlpatterns = [
    url(r'^search', views.TrpSearchView.as_view(), name="trp_search"),
    url(r'^hits', views.TrpSearchResultView.as_view(), name="trp_hits"),
    url(r'^docs', views.TrpListView.as_view(), name="trp_docs"),
    path('document/<col_id>/<doc_id>', views.TrpDocumentView.as_view(), name='trp_document'),
    path('page/<col_id>/<doc_id>/<page_id>', views.TrpPageView.as_view(), name='trp_page'),
]
