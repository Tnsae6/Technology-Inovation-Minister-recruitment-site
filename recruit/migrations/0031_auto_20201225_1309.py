# Generated by Django 2.2.3 on 2020-12-25 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0030_auto_20201222_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinfo',
            name='disablity',
            field=models.BooleanField(default=False, verbose_name='True if the person is disabled '),
        ),
    ]
