from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ..account.models import UserProfile
from ..blog.models import Category as BlogCategory, AbstractPost, AbstractCategory


class Category(AbstractCategory):
    pass


class Post(AbstractPost):
    CONTENT_TYPE = (
        (_('Free'), _('Free')),
        (_('Buyable'), _('Buyable')),
    )
    picture = models.ImageField(null=True, blank=True, upload_to='learning')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=10, choices=CONTENT_TYPE)
    purchaser = models.ManyToManyField(UserProfile)

    def get_absolute_url(self):
        return reverse('learning:slug', kwargs={'slug': self.slug})
