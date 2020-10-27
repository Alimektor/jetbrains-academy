"""hyperjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import MainView, AuthView, RegisterView, HomeView
from django.views.generic import RedirectView
from vacancy.views import VacancyMainView, VacancyView, VacancyCreateView
from resume.views import ResumeMainView, ResumeView, ResumeCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('vacancies/', VacancyMainView.as_view()),
    path('vacancies/<int:id_link>/', VacancyView.as_view()),
    path('resumes/', ResumeMainView.as_view()),
    path("resumes/<int:id_link>/", ResumeView.as_view()),
    path("login", AuthView.as_view()),
    path("signup", RegisterView.as_view()),
    path('login/', RedirectView.as_view(url='/login')),
    path('signup/', RedirectView.as_view(url='/signup')),
    path("home", HomeView.as_view()),
    path("resume/new", ResumeCreateView.as_view()),
    path("vacancy/new", VacancyCreateView.as_view()),
]
