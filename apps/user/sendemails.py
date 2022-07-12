
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.utils.html import strip_tags
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
from apps.user.otpgen import otp_, perform_otp_save


def send_otp(email):
    subject = 'Activate Your Django Account'
    # message = render_to_string('users/account_activation_email.html',{
    #     'otp': otp_,
    # })
    # template = strip_tags(message)
    # mail = EmailMultiAlternatives(subject,template,settings.EMAIL_HOST_USER,[email],)
    # mail.attach_alternative(message,"text/html")
    # mail.fail_silently = False
    # mail.send()
    sender = settings.EMAIL_HOST_USER
    message = f"Your verification code is {otp_}"
    send_mail(subject, message, sender, [email])
    perform_otp_save(email)
