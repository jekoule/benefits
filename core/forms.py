# -*- coding: utf-8 -*-
from django import forms


class SigninForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
