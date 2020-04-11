# Generated by Django 2.0 on 2020-04-09 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tamilmatrimony.models


class Migration(migrations.Migration):

    dependencies = [
        ('tamilmatrimony', '0002_auto_20200409_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShownInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pId', models.CharField(default='TMG', max_length=10)),
                ('intrestedPId', models.CharField(default='TMG', max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='profiles',
            name='image2',
            field=models.ImageField(blank=True, default='default/pimage.png', null=True, upload_to=tamilmatrimony.models.upload_location),
        ),
        migrations.AddField(
            model_name='profiles',
            name='image3',
            field=models.ImageField(blank=True, default='/media/default/pimage.png', null=True, upload_to=tamilmatrimony.models.upload_location),
        ),
        migrations.AddField(
            model_name='profiles',
            name='image4',
            field=models.ImageField(blank=True, default='/media/default/pimage.png', null=True, upload_to=tamilmatrimony.models.upload_location),
        ),
        migrations.AddField(
            model_name='profiles',
            name='native_city',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='profiles',
            name='native_dist',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='profiles',
            name='native_place',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='profiles',
            name='no_of_contacts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profiles',
            name='week_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='image',
            field=models.ImageField(blank=True, default='default/pimage.png', null=True, upload_to=tamilmatrimony.models.upload_location),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
