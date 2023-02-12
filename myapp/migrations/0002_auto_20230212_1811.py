# Generated by Django 3.2.16 on 2023-02-12 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votante',
            name='is_valid',
        ),
        migrations.AlterField(
            model_name='votante',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('PROCESSED', 'PROCESSED'), ('ERROR', 'ERROR')], max_length=10),
        ),
    ]
