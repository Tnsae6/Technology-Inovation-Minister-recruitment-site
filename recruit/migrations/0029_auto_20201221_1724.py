# Generated by Django 2.2.3 on 2020-12-21 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0028_auto_20201221_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edubackground',
            name='cumulative_gpa',
            field=models.CharField(max_length=10),
        ),
    ]
