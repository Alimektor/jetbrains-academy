from django.contrib import admin
from django.urls import path
from news.views import *
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView().get),
    path('news/<int:link>/', NewsView.as_view()),
    path("news/", NewsMainView.as_view()),
    path("news", RedirectView.as_view(url="news/")),
    path("news/create/", CreatingNewsView.as_view()),
    path("news/create", RedirectView.as_view(url="news/create/"))
]

