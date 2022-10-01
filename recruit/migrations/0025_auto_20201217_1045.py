# Generated by Django 2.2.3 on 2020-12-17 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0024_history_exam_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='exam_result',
            field=models.CharField(choices=[('pending', 'Pending'), ('Applicaton Initiated', 'Applicaton Initiated'), ('READY for EXAM', 'READY for EXAM'), ('DECLINED FOR EXAM', 'DECLINED FOR EXAM'), ('Passed for Exam', 'Passed for Exam'), ('Failed for Exam', 'Failed for Exam'), ('INTERVIEW SCHEDULED', 'INTERVIEW SCHEDULED'), ('INTERVIEW PASSED', 'INTERVIEW PASSED'), ('INTERVIEW FAILED', 'INTERVIEW FAILED')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='history',
            name='exam_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('Applicaton Initiated', 'Applicaton Initiated'), ('READY for EXAM', 'READY for EXAM'), ('DECLINED FOR EXAM', 'DECLINED FOR EXAM'), ('Passed for Exam', 'Passed for Exam'), ('Failed for Exam', 'Failed for Exam'), ('INTERVIEW SCHEDULED', 'INTERVIEW SCHEDULED'), ('INTERVIEW PASSED', 'INTERVIEW PASSED'), ('INTERVIEW FAILED', 'INTERVIEW FAILED')], default='Dectivate', max_length=100),
        ),
    ]
