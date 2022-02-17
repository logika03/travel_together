from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template import Template, Context
from django.urls import reverse

from searchpeople.celery import app

User = get_user_model()


@app.task
def send_mail_api(request):
    url = reverse('blog:articles')
    path = request.build_absolute_uri(url)
    user_emails = User.objects.values_list('email')
    template = Template(f'Посмотрите новые статьи {path}')
    send_mail("Search People", template.render(context=Context()),
              settings.EMAIL_HOST_USER,
              user_emails)


@app.task
def send_email_reset_password(user_id, user_email, request):
    url = reverse('change_password', args=[user_id])
    path = request.build_absolute_uri(url)
    template = Template(f'Для сброса пароля перейдите по ссылке {path}')
    message = template.render(context=Context({'user': user_id}))
    send_mail("Search People", message,
              settings.EMAIL_HOST_USER,
              [user_email, ])
