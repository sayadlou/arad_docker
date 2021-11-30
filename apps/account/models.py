from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser


class UserProfileManager(UserManager):
    pass


class UserProfile(AbstractUser):
    objects = UserProfileManager()

    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pic', default='default_profile.png')
    address = models.TextField(_('address'), max_length=150, default=_('your address'))
