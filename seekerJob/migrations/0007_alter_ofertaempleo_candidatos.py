# Generated by Django 3.2.9 on 2022-04-24 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seekerJob', '0006_alter_ofertaempleo_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertaempleo',
            name='Candidatos',
            field=models.ManyToManyField(blank=True, null=True, to='seekerJob.Usuario'),
        ),
    ]
