# Generated by Django 3.2.11 on 2022-01-12 19:55

import ckeditor_uploader.fields
import datetime
from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='learning.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Trash', 'Trash')], max_length=50)),
                ('view', models.BigIntegerField(blank=True, default=0, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.citext.CICharField(max_length=20), blank=True, size=None)),
                ('pub_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='learning')),
                ('type', models.CharField(choices=[('Free', 'Free'), ('Buyable', 'Buyable')], max_length=10)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learning.category')),
                ('purchaser', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
