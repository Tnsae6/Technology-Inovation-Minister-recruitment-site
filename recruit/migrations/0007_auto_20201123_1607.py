# Generated by Django 2.2.3 on 2020-11-23 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0006_auto_20201112_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinfo',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='quiz.Category'),
        ),
    ]