# Generated by Django 3.2.16 on 2023-04-24 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_customlink_etiqueta_etiquetavotante_inteciondevoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipio',
            name='latitude',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='latitude'),
        ),
        migrations.AddField(
            model_name='municipio',
            name='longitude',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='longitude'),
        ),
    ]
