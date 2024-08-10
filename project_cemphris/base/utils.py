from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.core.mail import EmailMessage
import asyncio
from project_cemphris.services import send_email
from project_cemphris.constants import DOMAIN, SITE_NAME, SUPPORT_EMAIL

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)

activation_token_manager = AccountActivationTokenGenerator()
password_reset_token_manager = PasswordResetTokenGenerator()

def send_password_reset_email(request, user):
    mail_subject = 'Password Reset Successful'
    reset_time = timezone.now()
    ip_address = request.META.get('HTTP_X_REAL_IP', None)
    context = {        
        'reset_time': reset_time,
        # 'location': location,
        'ip_address': ip_address,
        'site_name': SITE_NAME,
        'support_email': SUPPORT_EMAIL        
    }
    message = render_to_string('base/acc_pass_reset_email.html', context)
    to_email = user.email
    send_email.delay(subject=mail_subject, recipient=to_email, message=message)

def send_reset_password_email(request, user):    
    mail_subject = 'Reset Account Password'
    message = render_to_string('base/acc_reset_pass_email.html', {            
            'domain': DOMAIN,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': password_reset_token_manager.make_token(user),
        })
    to_email = user.email
    send_email.delay(subject=mail_subject, recipient=to_email, message=message)

def send_activation_mail(request, user):
    mail_subject = 'Activate your account.'
    message = render_to_string('base/acc_active_email.html', {            
            'domain': DOMAIN,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': activation_token_manager.make_token(user),
        })
    to_email = user.email
    send_email.delay(subject=mail_subject, recipient=to_email, message=message)

def send_instructor_login_details(request, user, school, password):    
    mail_subject = 'Login Credentials'
    message = render_to_string('base/login_cred_email.html', {
            'user': user,
            'school': school,
            'domain': DOMAIN,
            'password': password            
        })
    to_email = user.email
    send_email.delay(subject=mail_subject, recipient=to_email, message=message)