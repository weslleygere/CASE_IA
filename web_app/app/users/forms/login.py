from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    email = forms.CharField(
        label='E-mail',
        max_length=150,
        required=True,
        strip=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-mail',
            'autofocus': 'autofocus',
        })
    )

    password = forms.CharField(
        label='Senha',
        max_length=32,
        required=True,
        error_messages={
            'max_length': 'A senha não pode ter mais de 32 caracteres.', 
        },
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = User.objects.filter(username=email).first() or \
               User.objects.filter(email__iexact=email).first()

        if not user:
            raise forms.ValidationError("Usuário não encontrado.")
        else:
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is None:
                raise forms.ValidationError("Senha incorreta.")
            else:
                self.user = authenticated_user

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
