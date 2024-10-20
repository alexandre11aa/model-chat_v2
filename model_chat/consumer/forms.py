from django import forms
from django.db import transaction

from .models import CustomUser
from .validations import *

class UserForm(forms.Form):

    matricula = forms.IntegerField(
        label='Matrícula',
        widget=forms.NumberInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Matrícula',
        })
    )

    name = forms.CharField(
        label='Nome Completo',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Nome Completo',
        })
    )

    sexo = forms.ChoiceField(
        label='Sexo',
        choices=CustomUser.SEXO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control mb-3',
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Email',
        })
    )

    photo = forms.ImageField(
        label='Foto',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': 'image/*',
        })
    )

    def __init__(self, *args, **kwargs):
        
        # Aceitamos a instância do modelo 'CustomUser' como argumento opcional
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # Se uma instância for passada, populamos o formulário com seus valores
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['sexo'].initial = self.instance.sexo
            self.fields['email'].initial = self.instance.email
            self.fields['matricula'].initial = self.instance.matricula
            self.fields['photo'].initial = self.instance.photo

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_unique(email, instance=self.instance)
        return email

    @transaction.atomic
    def save(self, commit=True):

        # Se já houver uma instância, apenas atualize os dados da mesma
        user = self.instance if self.instance else CustomUser()

        # Extraindo dados do formulário e formatando conforme necessário
        matricula_formatting = remove_dot_hyphen_parentheses_espace_formatting(self.cleaned_data['matricula'])

        # Atualizando os campos do usuário
        user.name = self.cleaned_data['name']
        user.sexo = self.cleaned_data['sexo']
        user.email = self.cleaned_data['email']
        user.matricula = matricula_formatting
        user.photo = self.cleaned_data['photo']

        # Salvando o usuário no banco de dados
        if commit:
            user.save()

        return user