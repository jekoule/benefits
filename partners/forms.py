# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class SigninForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль',
                               max_length=32, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Войти',
                                     css_class='btn btn-block'))
        layout = self.helper.layout = Layout()
        for field_name, field in self.fields.items():
            layout.append(Field(field_name, placeholder=field.label))

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
