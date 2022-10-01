# Generated by Django 2.2.3 on 2020-12-01 07:57

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import recruit.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201113_1518'),
        ('recruit', '0009_auto_20201124_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinfo',
            name='EmailAdd_r',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='EmailAdd_r1',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='Name_r',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='Name_r1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='PhoneNumber_r',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='ET'),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='PhoneNumber_r1',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='ET'),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='docs',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[recruit.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='edubackground',
            name='Degree_level',
            field=models.CharField(choices=[('elementary', 'Elementary'), ('high School ', 'High School'), ('bsc', 'BSc'), ('msc', 'Msc'), ('phd', 'Phd')], max_length=10),
        ),
        migrations.CreateModel(
            name='Commitee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Profile')),
            ],
        ),
    ]