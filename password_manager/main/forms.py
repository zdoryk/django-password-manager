from django import forms


class PasswordEntryForm(forms.Form):
    service = forms.CharField()
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
