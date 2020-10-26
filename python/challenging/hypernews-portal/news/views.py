import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
from datetime import datetime
from .forms import *
from django.views.generic.base import View

from hypernews.settings import NEWS_JSON_PATH

date_format_from = "%Y-%m-%d %H:%M:%S"
date_format_to = "%Y-%m-%d"


class MainView:
    def get(self, request):
        return redirect("/news/")


class NewsMainView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        if query is None:
            query = ""
        context = {}
        search_form = SearchForm()
        context["form"] = search_form
        with open(NEWS_JSON_PATH, "r") as json_file:
            news_list = json.load(json_file)
        news_list.sort(key=lambda el: datetime.strptime(el["created"], date_format_from), reverse=True)
        news_group = {}
        for news in news_list:
            created = news["created"]
            link = news["link"]
            news_title = news["title"]
            if query not in news_title:
                continue
            title = datetime.strftime(datetime.strptime(created, date_format_from), date_format_to)
            if title in news_group:
                news_group[title].append((news_title, link))
            else:
                news_group[title] = [(news_title, link)]
        context["news_group"] = news_group.items()
        return render(request, "templates/hypernews/index.html", context)


class NewsView(TemplateView):
    template_name = "templates/hypernews/news.html"

    def get_context_data(self, link, **kwargs):
        context = super().get_context_data(**kwargs)
        with open(NEWS_JSON_PATH, "r") as json_file:
            news_list = json.load(json_file)
        for news in news_list:
            if int(link) == news["link"]:
                print(link, type(link))
                context["created"] = news["created"]
                context["text"] = news["text"]
                context["title"] = news["title"]
                break
        return context


class CreatingNewsView(View):
    def get(self, request, *args, **kwargs):
        creating_form = CreateNewsForm()
        form = {"form": creating_form}
        return render(request, "templates/hypernews/create.html", form)

    def post(self, request, *args, **kwargs):
        with open(NEWS_JSON_PATH, "r") as json_file:
            news_list = json.load(json_file)
        title = request.POST.get("title")
        text = request.POST.get("text")
        now = datetime.now()
        created = now.strftime(date_format_from)
        links = [int(i["link"]) for i in news_list]
        while True:
            link = random.randint(1, 10000)
            if link not in links:
                break
        news_list.append(
            {
                "created": created,
                "title": title,
                "text": text,
                "link": link
            }
        )
        with open(NEWS_JSON_PATH, "w") as json_file:
            json.dump(news_list, json_file)
        return redirect("/news/")
