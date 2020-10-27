from django import forms


class CreateNewForm(forms.Form):
    description = forms.CharField()
