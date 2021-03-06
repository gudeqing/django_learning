# Generated by Django 2.0.4 on 2018-04-13 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sangerdev', '0003_auto_20180411_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='webapi',
            name='controller',
            field=models.CharField(default='ref_rna_controller', max_length=100),
        ),
        migrations.AlterField(
            model_name='arg',
            name='arg_default',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='arg',
            name='arg_format',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='webapi',
            name='api_name',
            field=models.CharField(default='ref_rna.exp_venn', max_length=100),
        ),
        migrations.AlterField(
            model_name='webapi',
            name='package_rel_path',
            field=models.CharField(default='/wgcna/wgcna_prepare.py', max_length=200),
        ),
    ]
