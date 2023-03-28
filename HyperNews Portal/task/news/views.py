from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.conf import settings
import json
from collections import defaultdict
from django import forms
from django.views.generic.edit import FormView
from datetime import datetime
import random


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')

class NewsView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        articles_by_date = defaultdict(list)
        with open(settings.NEWS_JSON_PATH, 'r') as file:
            articles_list = json.load(file)
            for article in articles_list:
                if q and q.lower() in article['title'].lower():
                    date = article['created'].split()[0]
                    articles_by_date[date].append(article)
                elif not q:
                    date = article['created'].split()[0]
                    articles_by_date[date].append(article)
        articles_by_date = dict(sorted(articles_by_date.items(), reverse=True))
        return render(request, 'index.html', context={'articles_by_date': articles_by_date})

class NewsArticleView(View):
    def get(self, request, link):
        with open(settings.NEWS_JSON_PATH, 'r') as file:
            articles = json.load(file)
        for article in articles:
            if article['link'] == link:
                return render(request, 'list_item_page.html', article)

class CreateNewsForm(forms.Form):
    title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'placeholder': 'input title'}))
    text = forms.CharField(label="Text:", widget=forms.Textarea(attrs={'placeholder': 'input article text'}))

class CreateNewsFormView(FormView):
    form_class = CreateNewsForm
    template_name = 'news/create.html'
    success_url = '/news/'

    def form_valid(self, form):
        title = form.cleaned_data['title']
        text = form.cleaned_data['text']
        with open(settings.NEWS_JSON_PATH, 'r') as file:
            articles = json.load(file)
            article = {'created': datetime.now().strftime('%Y-%m-%d'), 'text': text, 'title': title, 'link': random.randint(10, 1000000)}
            articles.append(article)
        with open(settings.NEWS_JSON_PATH, 'w') as file:
            json.dump(articles, file)
        return redirect('/news/')
