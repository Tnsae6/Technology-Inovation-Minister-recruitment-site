# Generated by Django 2.2.3 on 2021-01-05 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0033_auto_20201230_0830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam_passed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='application',
            name='expired',
            field=models.BooleanField(default=False, verbose_name='if the date has paseed and Expired '),
        ),
        migrations.AlterField(
            model_name='history',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('Passed for Exam', 'Passed for Exam'), ('Failed for Exam', 'Failed for Exam'), ('Passed for INTERVIEW ', 'Passed for INTERVIEW '), ('Failed for INTERVIEW ', 'Failed for INTERVIEW'), ('INTERVIEW PASSED', 'INTERVIEW PASSED'), ('INTERVIEW FAILED', 'INTERVIEW FAILED')], default='pending', max_length=100),
        ),
    ]
