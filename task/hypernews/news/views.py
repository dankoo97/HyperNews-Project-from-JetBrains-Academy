from django.shortcuts import render
from django.views import View
from hypernews.settings import NEWS_JSON_PATH
from django.shortcuts import HttpResponse, Http404, redirect
from . import forms
import json
import datetime
import random
import re


def news_link(request, *args, **kwargs):
    news_dict = dict()
    link = kwargs['link']
    with open(NEWS_JSON_PATH) as news_json:
        news_dict = json.load(news_json)
    try:
        index = next(index for index, d, in enumerate(news_dict) if d['link'] == link)
    except StopIteration:
        raise Http404
    return render(request, 'news/link.html', context={'news': news_dict[index]})


def main_page(request):
    with open(NEWS_JSON_PATH) as news_json:
        articles = json.load(news_json)
    dates = set()
    search = ''
    if request.GET.get('q'):
        search = request.GET.get('q')
    index = 0
    while index < len(articles):
        if re.search(search, articles[index]['title']):
            dates.add(articles[index]['created'][:10])
            index += 1
        else:
            del articles[index]
    dates = list(dates)
    dates.sort(reverse=True)
    return render(request, 'news/main.html', context={'news': articles, 'dates': dates, 'search': forms.SearchForm})


def add_news_article(request):
    def create_link():
        link = random.randint(100000, 999999)
        with open(NEWS_JSON_PATH, 'r') as news_json:
            news_list = json.load(news_json)
        for links in news_list:
            if links['link'] == str(link):
                return create_link()
        return link
    if request.method == 'POST':
        form = forms.NewsForm(request.POST)
        if form.is_valid():
            article = {
                'title': request.POST.get('title'),
                'text': request.POST.get('text'),
                'created': str(datetime.datetime.now()),
                'link': str(create_link())
            }
            with open(NEWS_JSON_PATH, 'r') as news_json:
                data = json.load(news_json)
            data.append(article)
            with open(NEWS_JSON_PATH, 'w') as news_json:
                json.dump(data, news_json)
            return redirect('/news/')
    else:
        form = forms.NewsForm()

    return render(request, 'news/post.html', {'form': form})
