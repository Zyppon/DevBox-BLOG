# Generated by Django 4.2.7 on 2023-11-25 04:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='last_updated',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='published',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
