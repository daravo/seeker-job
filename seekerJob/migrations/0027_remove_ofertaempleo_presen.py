# Generated by Django 3.2.9 on 2022-05-13 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seekerJob', '0026_ofertaempleo_presen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ofertaempleo',
            name='Presen',
        ),
    ]
