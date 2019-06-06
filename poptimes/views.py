from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView

from .prtimes_api import get_release_list, get_entry, get_category_release_list, get_category

from .models import Message


class IndexView(TemplateView):
    template_name = 'poptimes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["release_list"] = get_release_list()
        return context


class CategoryView(TemplateView):
    template_name = 'poptimes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["release_list"] = get_category_release_list(
            self.kwargs['category_id'],
        )
        return context


@require_POST
def send_comment(request, company_id, release_id):
    try:
        comment = Message(
            company_id=company_id,
            release_id=release_id,
            text=request.POST['text']
        )
        comment.save()
    except Exception:
        return redirect(
            'poptimes:detail',
            company_id=company_id,
            release_id=release_id
        )
    else:
        return redirect(
            'poptimes:detail',
            company_id=company_id,
            release_id=release_id
        )


class EntryView(ListView):
    template_name = 'poptimes/entry.html'
    model = Message
    pagenate_by = 10

    def get_queryset(self):
        return Message.objects.filter(
            company_id=self.kwargs['company_id'],
            release_id=self.kwargs['release_id'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry"] = get_entry(
            self.kwargs['company_id'], self.kwargs['release_id'])
        return context
