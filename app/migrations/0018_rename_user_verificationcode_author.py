# Generated by Django 5.0 on 2023-12-19 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_verificationcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verificationcode',
            old_name='user',
            new_name='author',
        ),
    ]