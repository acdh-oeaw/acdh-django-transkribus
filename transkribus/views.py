from django.shortcuts import render

# Create your views here.
from django.conf import settings
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
        if result is not None:
            context['trp_result'] = result
            context['hits'] = result['numResults']
            context['rows'] = kwargs['rows']
            context['start'] = kwargs['start']
            context['base_url'] = f"{self.request.path}?query={query}"
            context['new_url'] = f"{self.request.path}?query={query}&filter={filterstring}"
            if int(context['rows']) + int(context['start']) < int(context['hits']):
                context['next'] = int(context['rows']) + int(context['start'])
            prev = int(context['start']) - int(context['rows'])
            if prev >= 0:
                context['prev'] = prev
            else:
                context['prev'] = 0
            return context


class TrpPageView(TemplateView):
    template_name = 'transkribus/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fulldoc_md = trp_get_fulldoc_md(
            base_url=base_url, user=user, pw=pw, **self.kwargs
        )
        result = get_transcript(fulldoc_md)
        context['result'] = result
        return context
