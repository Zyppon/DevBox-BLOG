# Generated by Django 4.2.7 on 2023-11-27 00:56

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_blogpost_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=martor.models.MartorField(),
        ),
    ]
