# Generated by Django 2.2.3 on 2021-01-17 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0049_delete_interview_schedule_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interview_schedule',
            name='application_userx',
        ),
        migrations.RemoveField(
            model_name='interview_schedule',
            name='history_userx',
        ),
        migrations.RemoveField(
            model_name='interview_schedule',
            name='interview_date',
        ),
        migrations.RemoveField(
            model_name='interview_schedule',
            name='interview_message',
        ),
        migrations.RemoveField(
            model_name='interview_schedule',
            name='interview_time',
        ),
        migrations.RemoveField(
            model_name='interview_schedule',
            name='time_set',
        ),
        migrations.AddField(
            model_name='interview_schedule',
            name='application_f',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recruit.Application'),
        ),
        migrations.AddField(
            model_name='interview_schedule',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interview_schedule',
            name='history_userx_f',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recruit.History', verbose_name='Interview Schedule Per User'),
        ),
        migrations.AddField(
            model_name='interview_schedule',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='interview_schedule',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='interview_schedule',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='interview_schedule',
            name='interview_location',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]