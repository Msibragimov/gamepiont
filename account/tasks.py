from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

from .utils import generate_token
from .models import Account


@shared_task
def send_email_on_registration(domain, uid):
    user = Account.objects.get(id=uid)
    token = generate_token.make_token(user)

    email_body = render_to_string('accounts/activation.html', context={'domain': domain, 'user': user, 'token': token})

    send_mail(
        'Activate your account',
        'message',
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=email_body
    )
