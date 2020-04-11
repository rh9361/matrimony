# Generated by Django 2.0 on 2020-04-09 18:02

from django.conf import settings
from django.db import migrations, models
import tamilmatrimony.models


class Migration(migrations.Migration):

    dependencies = [
        ('tamilmatrimony', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='annual_income',
            field=models.CharField(default='not specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='blood_group',
            field=models.CharField(default='not specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='dateOfBirth',
            field=models.DateTimeField(verbose_name='Date of Birth/Time - Format : YYYY-MM-DD HH:MM'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=15),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='image',
            field=models.ImageField(blank=True, default='/media/default/pimage.png', null=True, upload_to=tamilmatrimony.models.upload_location),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='maritalStatus',
            field=models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')], default='single', max_length=25),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='matrimonyProfileFor',
            field=models.CharField(choices=[('son', 'Son'), ('daughter', 'Daughter'), ('brother', 'Brother'), ('sister', 'Sister'), ('self', 'Self')], default='personal', max_length=25),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='pId',
            field=models.CharField(default='TMG', max_length=10),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='religion',
            field=models.CharField(choices=[('hindu', 'Hindu'), ('cristian', 'Cristian'), ('muslim', 'Muslim'), ('sikh', 'Sikh'), ('buddhist', 'Buddhist')], max_length=50),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='user',
            field=models.ForeignKey(default=1, on_delete=1, to=settings.AUTH_USER_MODEL),
        ),
    ]
