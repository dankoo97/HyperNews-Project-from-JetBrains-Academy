from django import forms


class NewsForm(forms.Form):
    title = forms.CharField(label='Title', max_length=64)
    text = forms.CharField(label='Text', max_length=512)


class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=64)
