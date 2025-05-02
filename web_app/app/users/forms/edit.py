from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserEditForm(forms.Form):
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
        error_messages={
            'max_length': 'O e-mail não pode ter mais de 100 caracteres.',
        },
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-mail',
            }
        )
    )

    phone = forms.CharField(  # ADICIONAR ISSO
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

    password1 = forms.CharField(
        label='Nova Senha',
        max_length=32,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nova Senha (Opcional)',
            }
        )
    )

    password2 = forms.CharField(
        label='Confirme a Nova Senha',
        max_length=32,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirme a Nova Senha (Opcional)',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Preencher os valores atuais
        if self.user:
            self.fields['full_name'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            self.fields['phone'].initial = self.user.last_name  # Aqui preenche o telefone

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if email and User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data

    def save(self):
        user = self.user
        user.first_name = self.cleaned_data['full_name']
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.last_name = self.cleaned_data['phone']

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])

        user.save()
        return user
