# Generated by Django 3.2.16 on 2023-08-27 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_campaign_municipios'),
    ]

    operations = [
        migrations.AddField(
            model_name='votanteprofile',
            name='validation_name',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Apellido Nombre'),
        ),
    ]
