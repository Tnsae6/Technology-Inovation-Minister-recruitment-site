# Generated by Django 2.2.3 on 2021-01-05 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0039_message'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='Messages',
        ),
    ]