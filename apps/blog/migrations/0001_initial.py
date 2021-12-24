# Generated by Django 3.2.9 on 2021-12-24 14:21

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', ckeditor.fields.RichTextField()),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Trash', 'Trash')], max_length=50)),
                ('view', models.BigIntegerField(blank=True, default=0, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('tag', models.CharField(max_length=50)),
                ('pub_date', models.DateField(auto_now=True)),
            ],
        ),
    ]