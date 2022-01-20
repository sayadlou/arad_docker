# Generated by Django 3.2.11 on 2022-01-12 19:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('subject', models.CharField(db_column='Subject', max_length=50)),
                ('phone', models.CharField(blank=True, db_column='Phone Number', max_length=15, null=True)),
                ('email', models.EmailField(db_column='Email Address', max_length=50)),
                ('content', models.TextField(db_column='Content', null=True)),
                ('checked', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], db_column='Read', default='No', max_length=50)),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
