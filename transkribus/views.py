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
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        if query is not None:
            try:
                result = trp_ft_search(
                    query, col_id=col_id, base_url=base_url, user=user, pw=pw
                )
            except Exception as e:
                context['trp_fetch_error'] = e
                print(e)
            else:
                context['trp_result'] = result
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
