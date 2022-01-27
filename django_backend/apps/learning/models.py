import datetime
from uuid import uuid4

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField, CICharField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from ..account.models import UserProfile
from ..blog.models import Category as BlogCategory
from config.settings.base import learning_attachments_path


class Category(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Post(models.Model):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    content = RichTextUploadingField()
    status = models.CharField(max_length=50, choices=STATUS)
    view = models.BigIntegerField(null=True, blank=True, default=0)
    tags = ArrayField(CICharField(max_length=20), blank=True)
    pub_date = models.DateField(_("Date"), default=datetime.date.today)
    picture = models.ImageField(null=True, blank=True, upload_to='learning/picture')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    max_order_quantity = models.DecimalField(max_digits=12, decimal_places=0)
    min_order_quantity = models.DecimalField(max_digits=12, decimal_places=0)
    purchaser = models.ManyToManyField(UserProfile)
    video = models.ForeignKey('VideoFile', on_delete=models.CASCADE, null=True, blank=True)
    attachment = models.FileField(null=True, blank=True, storage=learning_attachments_path)

    def get_absolute_url(self):
        return reverse('learning:slug', kwargs={'slug': self.slug})
    def __str__(self):
        return f'{self.title}'

class VideoFile(models.Model):
    name = models.CharField(max_length=255)
    arvan_id = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'
