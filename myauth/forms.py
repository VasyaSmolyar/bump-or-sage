from django.forms import CharField, Form, PasswordInput, EmailField
from django import forms
from django.contrib.auth.validators import ASCIIUsernameValidator

class RegForm(Form):
    login = CharField(label='Login:',max_length=100,
        error_messages = {'required' : 'Укажите логин',
            'invalid' : 'Логин должен содержать только латинские символы и цифры '},
        widget = forms.TextInput(attrs = {'class' : 'form-control'}),
        validators = [ASCIIUsernameValidator()])
    email = EmailField(label='Email:',max_length=100,
        widget = forms.EmailInput(attrs = {'class' : 'form-control'}),
        error_messages = {'required' : 'Укажите email','invalid' : 'Введите валидный email' })
    pwd = CharField(label='Password:',max_length=100,
        error_messages = {'required' : 'Укажите пароль',
            'invalid' : 'Пароль должен содержать только латинские символы и цифры '},
        widget = PasswordInput(attrs = {'class' : 'form-control'}),
        validators = [ASCIIUsernameValidator()])
    pwd2 = CharField(label='Password again:',max_length=100,
        error_messages = {'required' : 'Укажите пароль ещё раз',},
        widget = PasswordInput(attrs = {'class' : 'form-control'}))

    def clean(self):
        if self.cleaned_data.get('pwd') != self.cleaned_data.get('pwd2'):
            raise forms.ValidationError('Пароли должны совпадать!')
        return self.cleaned_data
