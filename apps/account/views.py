from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django import forms
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.account.models import UserProfile

from .forms import MyAuthenticationForm, MyPasswordResetForm, MyPasswordChangeForm


class Login(LoginView):
    form_class = MyAuthenticationForm
    template_name = 'account/login.html'


class Logout(LogoutView):
    template_name = 'account/logged_out.html'


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change_form.html'
    form_class = MyPasswordChangeForm


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'


class PasswordReset(PasswordResetView):
    subject_template_name = 'account/password_reset_subject.txt'
    email_template_name = 'account/password_reset_email.html'
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    form_class = MyPasswordResetForm


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('account:password_reset_complete')
    template_name = 'account/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class Profile(LoginRequiredMixin, DetailView):
    model = UserProfile
    login_url = reverse_lazy('account:login')
    template_name = "account/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user
