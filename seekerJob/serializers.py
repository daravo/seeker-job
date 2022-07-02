from rest_framework import serializers

from .models import *

class CanalMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CanalMensaje
        fields=("__all__")

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username"]