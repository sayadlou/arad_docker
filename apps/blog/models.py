from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField, CICharField
from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
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
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    status = models.CharField(max_length=50, choices=STATUS)
    view = models.BigIntegerField(null=True, blank=True, default=0)
    picture = models.ImageField(null=True, blank=True, upload_to='blog')
    tags = ArrayField(CICharField(max_length=20), blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateField(_("Date"), default=datetime.date.today)

    def __str__(self):
        return self.title
