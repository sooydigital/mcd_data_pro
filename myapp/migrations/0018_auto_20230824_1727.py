# Generated by Django 3.2.16 on 2023-08-24 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_votanteprofile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='votante',
            name='coordinador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Coordinador', to='myapp.votante'),
        ),
        migrations.AlterField(
            model_name='votante',
            name='lider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Leader', to='myapp.votante'),
        ),
    ]
