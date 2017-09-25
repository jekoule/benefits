# -*- coding: utf-8 -*-
from django import forms
from .models import Member


class MemberRegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number', 'date_of_birth']

    password = forms.CharField(max_length=32, label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, label='Повтор пароля',
                                widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(MemberRegisterForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError('Введенные пароли не совпадают')


class MemberChangeForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number', 'date_of_birth']


class SigninForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
