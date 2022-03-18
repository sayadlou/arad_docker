# Generated by Django 3.2.12 on 2022-03-18 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('azbankgateways', '0004_auto_20220318_0959'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='azbankgateways.bank'),
        ),
    ]
