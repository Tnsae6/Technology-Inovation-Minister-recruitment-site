# Generated by Django 2.2.3 on 2021-01-18 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0052_interview_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview_schedule',
            name='history_userx_f',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recruit.History', verbose_name='Interview Schedule Per User'),
        ),
    ]