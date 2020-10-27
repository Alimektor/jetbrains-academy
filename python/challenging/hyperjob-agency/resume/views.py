from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import resumes
from django.http import HttpResponseForbidden


class ResumeMainView(View):
    def get(self, request, *args, **kwargs):
        data = {
            "title": "Vacancies",
            "list": resumes
        }
        return render(request, template_name="list.html", context=data)


class ResumeView(View):
    def get(self, request, id_link, *args, **kwargs):
        vacancy = resumes.get(id=id_link)
        data = {
            "title": f"Author: {vacancy.author}",
            "author": vacancy.author,
            "description": vacancy.description
        }
        return render(request, template_name="authors.html", context=data)


class ResumeCreateView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
        if not request.user:
            return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
        author = request.user
        description = request.POST.get("description")
        resume = resumes.create(
            author=author,
            description=description
        )
        resume.save()
        return redirect("/home")
