import django_filters

from .models import *

class OfertaFilter(django_filters.FilterSet):
    class Meta:
        model=OfertaEmpleo
        fields=["Presencialidad", "Estudios", "Jornada", "Puesto", "Contrato"]