# Generated by Django 2.0.1 on 2018-02-06 17:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20180206_1816'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CommentChield',
            new_name='CommentChild',
        ),
    ]
