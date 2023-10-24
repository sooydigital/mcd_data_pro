# Generated by Django 3.2.16 on 2023-10-24 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_municipio_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='municipio',
            name='link',
        ),
        migrations.AddField(
            model_name='puestovotacion',
            name='link',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
