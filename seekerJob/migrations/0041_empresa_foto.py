# Generated by Django 3.2.9 on 2022-06-18 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seekerJob', '0040_usuario_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='Foto',
            field=models.ImageField(default='user-default.png', upload_to='', verbose_name='Imagen de Perfil'),
        ),
    ]
