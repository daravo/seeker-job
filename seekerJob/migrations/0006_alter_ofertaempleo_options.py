# Generated by Django 3.2.9 on 2022-04-24 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seekerJob', '0005_ofertaempleo_candidatos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ofertaempleo',
            options={'permissions': (('aplicar_como_candidato', 'aplicar_como_candidato'),)},
        ),
    ]
