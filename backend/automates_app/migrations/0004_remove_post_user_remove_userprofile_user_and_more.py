# Generated by Django 5.1.3 on 2024-12-04 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('automates_app', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Draft',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
