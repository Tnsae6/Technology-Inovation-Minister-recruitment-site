# Generated by Django 2.2.3 on 2020-12-21 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0027_auto_20201221_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edubackground',
            name='cumulative_gpa',
            field=models.CharField(default='NOT PROVIDED', max_length=10),
        ),
        migrations.AlterField(
            model_name='edubackground',
            name='edubackground',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personaledu', to='recruit.PersonalInfo'),
        ),
        migrations.AlterField(
            model_name='elementary_school',
            name='pinfoe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_elementary', to='recruit.PersonalInfo'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personalexxp', to='recruit.PersonalInfo'),
        ),
        migrations.AlterField(
            model_name='languageskills',
            name='languageskills',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personallangu', to='recruit.PersonalInfo'),
        ),
        migrations.AlterField(
            model_name='preparatory_school',
            name='pinfop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_preparatory', to='recruit.PersonalInfo'),
        ),
        migrations.AlterField(
            model_name='secondary_school',
            name='pinfos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_Secondary', to='recruit.PersonalInfo'),
        ),
    ]
