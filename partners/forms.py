# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate


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
        if not user_cache.is_partner:
            raise forms.ValidationError('У вашей учетной записи недостаточно прав \
                                  для просмотра данной страницы')
