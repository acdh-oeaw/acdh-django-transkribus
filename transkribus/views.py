from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from transkribus.trp_utils import (
    user,
    pw,
    col_id,
    base_url,
    trp_login,
    trp_ft_search,
    trp_get_fulldoc_md,
    get_transcript,
    list_documents,
    trp_get_doc_overview_md,
    crowd_base_url
)

TRP_PUBLIC = getattr(settings, 'TRANSKRIBUS_PUBLIC', False)

try:
    APIS_OSD_JS = settings.APIS_OSD_JS
except AttributeError:
    APIS_OSD_JS = (
        "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/2.4.0/openseadragon.min.js"
    )
try:
    APIS_OSD_IMG_PREFIX = settings.APIS_OSD_IMG_PREFIX
except AttributeError:
    APIS_OSD_IMG_PREFIX = (
        "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/2.4.0/images/"
    )


class TrpSearchView(TemplateView):
    template_name = 'transkribus/search.html'


class TrpSearchResultView(TemplateView):
    template_name = 'transkribus/hits.html'

    def get_context_data(self, **kwargs):
        additional_filters = [f"collectionId:{col_id}", ]
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('filter'):
            additional_filters.append(self.request.GET.get('filter'))
        print(f"additional_filters: {additional_filters}")
        query = self.request.GET.get('query')
        kwargs = {
            'query': query,
            'filter': set(additional_filters),
            'start': self.request.GET.get('start', '0'),
            'rows': self.request.GET.get('rows', '25')
        }
        filterstring = "&filter=".join(additional_filters)
        try:
            result = trp_ft_search(
                base_url, user, pw, **kwargs
            )
        except Exception as e:
            context['trp_fetch_error'] = e
            print(e)
            result = None
        if result:
            context['trp_result'] = result
            context['hits'] = result['numResults']
            context['rows'] = kwargs['rows']
            context['start'] = kwargs['start']
            context['base_url'] = f"{self.request.path}?query={query}"
            if "f_title" in filterstring:
                context['clear_filter'] = True
            context['new_url'] = f"{self.request.path}?query={query}&filter={filterstring}"
            if int(context['rows']) + int(context['start']) < int(context['hits']):
                context['next'] = int(context['rows']) + int(context['start'])
            prev = int(context['start']) - int(context['rows'])
            if prev >= 0:
                context['prev'] = prev
            else:
                context['prev'] = 0
            return context


class TrpListView(UserPassesTestMixin, TemplateView):
    template_name = 'transkribus/documents.html'

    def test_func(self):
        if self.request.user.is_authenticated or TRP_PUBLIC:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = list_documents(base_url=base_url, col_id=col_id, user=user, pw=pw)
        try:
            context['collection'] = result[0]['collectionList']['colList'][0]
        except IndexError:
            context['collection'] = None
        context['result'] = result
        context['nr_docs'] = len(result)
        context['col_id'] = col_id
        return context


class TrpDocumentView(UserPassesTestMixin, TemplateView):
    template_name = 'transkribus/doc_overview.html'

    def test_func(self):
        if self.request.user.is_authenticated or TRP_PUBLIC:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doc_md'] = trp_get_doc_overview_md(
            base_url=base_url, user=user, pw=pw, **self.kwargs
        )
        context['col_id'] = self.kwargs['col_id']
        context['doc_id'] = self.kwargs['doc_id']
        context['edit_link'] = crowd_base_url.format(
            self.kwargs['col_id'],
            self.kwargs['doc_id'],
            '1'
        )
        return context


class TrpPageView(UserPassesTestMixin, TemplateView):
    template_name = 'transkribus/page.html'

    def test_func(self):
        if self.request.user.is_authenticated or TRP_PUBLIC:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fulldoc_md = trp_get_fulldoc_md(
            base_url=base_url, user=user, pw=pw, **self.kwargs
        )
        result = get_transcript(fulldoc_md)
        page_id = int(self.kwargs['page_id'])
        context['result'] = result
        context['first_page'] = reverse('transkribus:trp_page', kwargs={
            'col_id': result['col_id'],
            'doc_id': result['doc_id'],
            'page_id': '1'
        })
        context['last_page'] = reverse('transkribus:trp_page', kwargs={
            'col_id': result['col_id'],
            'doc_id': result['doc_id'],
            'page_id': result['extra_info']['nrOfPages']
        })
        if page_id > 1:
            context['prev'] = reverse('transkribus:trp_page', kwargs={
                'col_id': result['col_id'],
                'doc_id': result['doc_id'],
                'page_id': f"{page_id-1}"
            })
        else:
            context['prev'] = None

        if page_id < int(result['extra_info']['nrOfPages']):
            context['next'] = reverse('transkribus:trp_page', kwargs={
                'col_id': result['col_id'],
                'doc_id': result['doc_id'],
                'page_id': f"{page_id+1}"
            })
        else:
            context['next'] = None

        context['openseadragon_js'] = APIS_OSD_JS
        context['openseadragon_img'] = APIS_OSD_IMG_PREFIX
        context['edit_link'] = crowd_base_url.format(
            self.kwargs['col_id'],
            self.kwargs['doc_id'],
            page_id
        )
        return context
