# Generated by Django 3.2.16 on 2023-02-13 15:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_customuser_municipio'),
    ]

    operations = [
        migrations.AddField(
            model_name='votante',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
