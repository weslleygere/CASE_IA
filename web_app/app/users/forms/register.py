from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.Form):
    full_name = forms.CharField(
        label='Nome Completo',
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome Completo',
                'autofocus': 'autofocus',
            }
        )
    )

    email = forms.EmailField(
        label='E-mail',
        max_length=100,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-mail',
            }
        )
    )

    phone = forms.CharField(
        label='Telefone',
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Telefone',
            }
        )
    )

    password = forms.CharField(
        label='Senha',
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Senha',
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['full_name'], 
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.last_name = self.cleaned_data['phone']
        user.save()
        return user