from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, PasswordChangeForm, \
    SetPasswordForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField

from .widget import CustomCaptchaTextInput


class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': "form-control"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': "form-control"}),
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': "form-control"})
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': "form-control", 'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))


class MySetPasswordForm(SetPasswordForm):
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
    )