from django.db import models
from django.db.models import CharField, ForeignKey
from django.contrib.auth.models import User


class Vacancy(models.Model):
    description = CharField(max_length=1024)
    author = ForeignKey(User, related_name="vacancy_user", on_delete=models.CASCADE)

vacancies = Vacancy.objects