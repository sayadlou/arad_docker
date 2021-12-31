from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField, CICharField
import datetime

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class AbstractCategory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        abstract = True


class Category(AbstractCategory):
    pass


class AbstractPost(models.Model):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )
    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    status = models.CharField(max_length=50, choices=STATUS)
    view = models.BigIntegerField(null=True, blank=True, default=0)
    tags = ArrayField(CICharField(max_length=20), blank=True)
    pub_date = models.DateField(_("Date"), default=datetime.date.today)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Post(AbstractPost):
    picture = models.ImageField(null=True, blank=True, upload_to='blog')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('blog:slug', kwargs={'slug': self.slug})
