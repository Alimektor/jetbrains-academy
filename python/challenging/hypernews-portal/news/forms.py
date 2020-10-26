from django import forms


class CreateNewsForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField()


class SearchForm(forms.Form):
    q = forms.CharField(label="Search")
