from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django import forms
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.account.models import UserProfile

from .forms import MyAuthenticationForm, MyPasswordResetForm


class Login(LoginView):
    form_class = MyAuthenticationForm


class Logout(LogoutView):
    pass


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')


class PasswordChangeDone(PasswordChangeDoneView):
    pass


class PasswordReset(PasswordResetView):
    success_url = reverse_lazy('account:password_reset_done')
    form_class = MyPasswordResetForm


class PasswordResetDone(PasswordResetDoneView):
    pass


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('account:password_reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    pass


class Profile(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "registration/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user
