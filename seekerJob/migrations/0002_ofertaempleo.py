# Generated by Django 3.2.9 on 2022-04-15 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seekerJob', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfertaEmpleo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=30)),
                ('Descripcion', models.CharField(max_length=100)),
                ('UltimoDiaInscripcion', models.DateField(auto_now=True)),
                ('EmpresaSolicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seekerJob.empresa')),
            ],
        ),
    ]
