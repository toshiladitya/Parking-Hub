from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage,EmailMultiAlternatives
import os
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



def send_verification_mail(instance):
    breakpoint()
    subject = "Confirm Your Email Address"
    text_content = f"Hello {instance.full_name}!\n\nThank you for registering on our website. Please confirm your email address to activate your account.\n\nClick the following link to activate your account:\n"
    from_email = settings.EMAIL_HOST_USER
    to_list = [instance.email]
    uid = urlsafe_base64_encode(force_bytes(instance.uuid))
    verify_url = reverse('admin_verify_email') + f'?uid={uid}'
    html_content = text_content + f"<a href='http://127.0.0.1:8000/api/v1{verify_url}'>Click Here</a>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

class Utils:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['body'],
            from_email=os.getenv('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.content_subtype = 'html'
        email.send()

