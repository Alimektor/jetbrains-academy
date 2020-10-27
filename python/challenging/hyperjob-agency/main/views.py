from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from forms import CreateNewForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        links = {
            "/login": "Login",
            "/signup": "Sign up",
            "/vacancies": "Vacancies",
            "/resumes": "Resumes",
            "/home": "Home",
        }
        context["links"] = links.items()
        return context


class AuthView(LoginView):
    redirect_authenticated_user = True
    template_name = "login.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = "login"
    template_name = "signup.html"


class HomeView(View):
    def get(self, request, *artgs, **kwargs):
        form = CreateNewForm()
        title = "Create new resume"
        link = "/resume/new"
        if User.is_staff:
            title = "Create new vacancy"
            link = "/vacancy/new"
        data = {
            "title": title,
            "action_link": link,
            "form": form
        }
        return render(request, template_name="create.html", context=data)
