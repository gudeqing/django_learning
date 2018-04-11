# Generated by Django 2.0.4 on 2018-04-11 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sangerdev', '0002_auto_20180411_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='webapi',
            name='description',
            field=models.CharField(default='simple description', max_length=500),
        ),
        migrations.AddField(
            model_name='webapi',
            name='package_rel_path',
            field=models.CharField(default='/*/*.py', max_length=200),
        ),
        migrations.AlterField(
            model_name='webapi',
            name='api_name',
            field=models.CharField(default='xa_xb', max_length=100),
        ),
    ]
