# Generated by Django 2.2.3 on 2020-12-12 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201113_1518'),
        ('recruit', '0013_auto_20201210_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='expired',
            field=models.BooleanField(default=False, verbose_name='if the date has paseed and recruited '),
        ),
        migrations.CreateModel(
            name='Recruit_Application_Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pending', models.BooleanField(verbose_name=' if the user has applied for specfic application but still waiting for evaluation ')),
                ('falied', models.BooleanField(default=False, verbose_name='if the applicants has falied  specfic applicaton its active then  ')),
                ('exam_active', models.BooleanField(default=False, verbose_name='active exam for applicant  ')),
                ('exam_taken', models.BooleanField(default=False, verbose_name='if the applicants has taken the exam and waitng for result  ')),
                ('exam_result_pending', models.BooleanField(default=False, verbose_name='if the applicants has taken the exam and waitng for result  ')),
                ('passed_the_exam', models.BooleanField(default=False, verbose_name='if the applicants has passed the exam')),
                ('falied_the_exam', models.BooleanField(default=False, verbose_name='if the applicants has falied the exam')),
                ('interview_passed', models.BooleanField(default=False, verbose_name='if the applicants has passed the interview ')),
                ('interview_falied', models.BooleanField(default=False, verbose_name='if the applicants has falied the interview ')),
                ('jump_to_interview', models.BooleanField(default=False, verbose_name='if the applicants pass directly to interview e.g interns  ')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='recruit.Application')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Profile')),
            ],
        ),
    ]
