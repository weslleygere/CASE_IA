from django import forms
import logging
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings

logger = logging.getLogger(__name__)

class PasswordResetForm(forms.Form):
    success_message = "E-mail de redefinição de senha enviado com sucesso."
    error_message = "Erro ao enviar e-mail de redefinição de senha."

    email = forms.CharField(
        label="E-mail",
        max_length=150,
        required=True,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "E-mail",
                "autofocus": "autofocus",
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        user = User.objects.filter(username=email).first() or \
            User.objects.filter(email__iexact=email).first()

        if not user:
            raise forms.ValidationError("Nenhum usuário encontrado com esse e-mail.")
        else:
            self.user = user

        return cleaned_data

    def send_reset_email(self, request):
        user = self.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = request.build_absolute_uri(
            reverse("reset_password_change", kwargs={"uidb64": uid, "token": token})
        )

        subject = "Instruções para redefinição de senha"
        message = (
            f"Olá {user.username},\n\n"
            f"Para redefinir sua senha, clique no link abaixo:\n\n{reset_url}\n\n"
            "Se você não solicitou isso, ignore este e-mail."
        )

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]

        try:
            email = EmailMessage(subject, message, from_email, to_email)
            email.send()
            return True
        except Exception as e:
            logger.error("Erro ao enviar e-mail de redefinição de senha: %s", e)
            return False