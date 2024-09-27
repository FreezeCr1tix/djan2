from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import F
from django.utils.safestring import mark_safe

from .models import News


def censor(text):
    """Фильтр, заменяющий нежелательные слова на символы "*".
    """
    bad_words = ['еблан', 'мудак', 'хуйло']
    for word in bad_words:
        text = text.replace(word, '*' * len(word))
    return text


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-date_published']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            short_text=F('text')[:20], # Обрезаем текст до 20 символов
            censored_title=mark_safe(censor(F('title'))),
            censored_text=mark_safe(censor(F('text'))),
        )
        return queryset


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, *kwargs):
        context = super().get_context_data(*kwargs)
        context['news'].title = censor(context['news'].title)
        context['news'].text = censor(context['news'].text)
        context['news'].date_published = context['news'].date_published.strftime("%d.%m.%Y")
        return context
