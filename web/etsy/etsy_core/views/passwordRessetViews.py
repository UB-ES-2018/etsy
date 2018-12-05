from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.mail import send_mail
from django.views.generic import *
from django.shortcuts import render, redirect
from ..models import User 
from ..forms import RecoveryForm, PasswordResetForm
import sys

def password_reset(request):
    '''
    Send a recovery password email with a unique validation token to the user
    '''
    context = {}
    if request.method == 'GET':
        form = RecoveryForm()
    if request.method == 'POST':
        form = RecoveryForm(request.POST)
        if form.is_valid():
            email_template_name='auth/password_reset_email.html'   
            email_ = form.cleaned_data['email']
            associated_user = User.objects.get(email=email_)
            email_context = {
                'email': associated_user.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'Etsy',
                'uid': urlsafe_base64_encode(force_bytes(associated_user.id)).decode(),
                'user': associated_user,
                'token': default_token_generator.make_token(associated_user),
                'protocol': 'http',
            }
            email = loader.render_to_string(email_template_name, email_context)
            send_mail('Etsy password recovery', email, 'sender@example.com', [associated_user.email], fail_silently=False)
    
    context['form'] = form
    return render(request, 'auth/password_reset_form.html', context)

def password_confirm(request, uidb64=None, token=None):
    if request.method == 'GET':
        form = PasswordResetForm()
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                return redirect('login')
        else:
            form.add_error("new_password1", "The reset password link is no longer valid")
    
    return render(request, 'auth/password_confirm_form.html', {'form': form})