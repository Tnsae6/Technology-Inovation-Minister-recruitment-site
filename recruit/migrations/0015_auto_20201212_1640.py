# Generated by Django 2.2.3 on 2020-12-12 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0014_auto_20201212_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='qualifaction',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
