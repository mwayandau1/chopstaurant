from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def getAccountUrl(request):
    if request.user.role == 1:
        redirectUrl = 'vendor-dashboard'
        return redirectUrl
    elif request.user.role == 2:
        redirectUrl = 'customer-dashboard'
        return redirectUrl
    elif request.user.role == None and request.user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


def send_email_verification(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    # mail_subject = "Please click on the link to activate your account"
    message = render_to_string(email_template,
                               {
                                   'user': user,
                                   'domain': current_site,
                                   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                   'token': default_token_generator.make_token(user),

                               })
    to_email = user.email
    mail = EmailMessage(mail_subject, message,
                        from_email=from_email, to=[to_email])
    mail.send()


def send_email_approval(mail_subject, email_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = context['user'].email
    message = render_to_string(email_template, context)
    mail = EmailMessage(mail_subject, message,
                        from_email=from_email, to=[to_email])
    mail.send()
