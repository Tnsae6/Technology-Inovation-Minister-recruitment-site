# Generated by Django 2.2.3 on 2020-12-25 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0031_auto_20201225_1309'),
        ('quiz', '0002_auto_20201217_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='historyx',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recruit.History', verbose_name='applicationc'),
        ),
    ]
