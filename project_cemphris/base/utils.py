from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
import asyncio
from project_cemphris.services import schedule_email, send_email

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)

activation_token_manager = AccountActivationTokenGenerator()

def send_activation_mail(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('base/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': activation_token_manager.make_token(user),
        })
    to_email = user.email

    res = send_email(subject=mail_subject, recipient=to_email, message=message)
    return res

def send_instructor_login_details(request, user, school, password):
    current_site = get_current_site(request)
    mail_subject = 'Login Credentials'
    message = render_to_string('base/login_cred_email.html', {
            'user': user,
            'school': school,
            'domain': current_site.domain,
            'password': password            
        })
    to_email = user.email
    
    email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
    email.send()