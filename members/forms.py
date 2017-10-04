# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from .models import Member


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number', 'date_of_birth']

    password = forms.CharField(max_length=32, label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, label='Повтор пароля',
                                widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError('Введенные пароли не совпадают')


class EditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number', 'date_of_birth']


class SigninForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SigninForm, self).clean()
        email = cleaned_data['email']
        password = cleaned_data['password']
        user_cache = authenticate(username=email, password=password)
        if user_cache is None:
            raise forms.ValidationError('Вы ввели неверный e-mail или пароль')
        if not user_cache.is_member:
            raise forms.ValidationError('У вашей учетной записи недостаточно прав \
                                  для просмотра данной страницы')
