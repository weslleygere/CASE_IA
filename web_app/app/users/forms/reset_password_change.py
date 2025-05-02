from django import forms
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

class PasswordChangeForm(forms.Form):
    error_message = "O link de redefinição de senha é inválido ou expirou."
    success_message = "Senha alterada com sucesso."
    
    new_password = forms.CharField(
        label="Nova Senha",
        max_length=32,
        required=True,
        error_messages={
            "max_length": "A senha não pode ter mais de 32 caracteres.",
        },
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Nova Senha",
            "autofocus": "autofocus",
        })
    )
    confirm_new_password = forms.CharField(
        label="Confirme a Nova Senha",
        max_length=32,
        required=True,
        error_messages={
            "max_length": "A senha não pode ter mais de 32 caracteres.",
        },
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirme a Nova Senha",
        })
    )

    def __init__(self, uidb64, token, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uidb64 = uidb64
        self.token = token
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

    def is_valid_token(self):
        try:
            uid = urlsafe_base64_decode(self.uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return False

        if default_token_generator.check_token(user, self.token):
            self.user = user
            return True
        return False

    def save(self):
        self.user.set_password(self.cleaned_data["new_password"])
        self.user.save()
        return self.user

