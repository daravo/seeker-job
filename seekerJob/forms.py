from cProfile import label
from dataclasses import fields
from datetime import date
from pyexpat import model



from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from seekerJob.models import Empresa, ExperienciaLaboral, Idiomas, OfertaEmpleo, Titulos, Usuario 
import datetime
from django.core.exceptions import ValidationError

class RegistroUsuarioEmpresaForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            "username",
            "email",
        ]
        labels={
            "username": "login de la empresa",
            "email": "email de la empresa",
        }

class RegistroEmpresaForm(ModelForm):
    class Meta:
        model=Empresa
        fields=[
            "nombre_empresa",
            "telefono",
        ]
        label={
            "nombre_empresa": "nombre de la empresa",
            "telefono" : "telefono de la empresa",
        }

class RegistroOfertaEmpleo(ModelForm):
    class Meta:
        model=OfertaEmpleo
        fields=[
            "Titulo",
            "Descripcion",
            "UltimoDiaInscripcion",
            "Presencialidad",
            "Estudios",
            "Jornada",
            "Puesto",
            "Contrato"
        ]
        labels={
            "Descripcion":"Descripcion del trabajo",
            "UltimoDiaInscripcion":"Ultimo dia de Inscripcion"
        }
        widgets={
            "UltimoDiaInscripcion": forms.DateInput(
                attrs={
                    "type":"date",
                }
            )
        }
    def clean_UltimoDiaInscripcion(self):
        data=self.cleaned_data["UltimoDiaInscripcion"]

        if data < datetime.date.today() +datetime.timedelta(days=7):
            raise ValidationError(("Fecha invalida, por favor escriba una fecha posterior al dia de hoy"))

        return data
        

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            "username",
            "email",
        ]
        labels={
            "username": "login del usuario",
            "email": "email del usuario",
        }

class RegistroUsuario2Form(ModelForm):
    class Meta:
        model=Usuario
        fields=[
            "nombre",
            "apellido",
            "anioNacimiento",
            
        ]
        labels={
            "anioNacimiento":"Fecha de nacimiento",
           
        }
        widgets={
            "anioNacimiento": forms.DateInput(
                attrs={
                    "class": "m-2",
                    "type":"date",
                }
            ),
            "nombre": forms.TextInput(
                attrs={
                    "class": "m-2",
                }
            ),
            "apellido": forms.TextInput(
                attrs={
                    "class": "m-2",
                }
            ),
            
        }

class FormMensaje(forms.Form):
    mensaje=forms.CharField(widget=forms.Textarea(attrs={
        "class": "formulario_ms fs-4 d-block p-3 my-1",
        "placeholder": "Escribe tu mensaje",
        "rows": "3",
        "onfocus":"clearInterval(setTimeout)"
    }))

class FormTitulos(ModelForm):
    def clean(self):
        data=self.cleaned_data["FechaInicio"]
        data2=self.cleaned_data["FechaFinFinal"]

        if data >data2:
             raise ValidationError({"FechaInicio": ("La fecha no puede ser menor que la fecha fin")})
       
    class Meta:
        model=Titulos
        fields=["InstitucionEducativa","Titulo", "FechaInicio", "FechaFinFinal"]
        labels={
            "InstitucionEducativa":"Institucion Educativa",
            "FechaInicio": "Fecha de Inicio",
            "FechaFinFinal": "Fecha de Fin",
        }
        widgets={
           "InstitucionEducativa":forms.TextInput(
                attrs={
               
                    "class":"m-2",
                }
            ),
           "Titulo":forms.TextInput(
                attrs={
               
                    "class":"m-2",
                }
            ),
            
            "FechaInicio":forms.DateInput(
                attrs={
                    "type":"date",
                    "class":"m-2",
                }
            ),
            "FechaFinFinal":forms.DateInput(
                attrs={
                    "type":"date",
                    "class":"m-2",
                }
            ),

        }


class FormIdioma(ModelForm):
    class Meta:
        model=Idiomas
        fields=["Idioma","nivel"]
        labels={
            "nivel":"Nivel"
        }
        widgets={
            "Idioma":forms.TextInput(
                attrs={
                    "class": "m-2",
                }
            ),
            
        }
    
class FormExperienciaLaboral(ModelForm):
    def clean(self):
        data=self.cleaned_data["FechaInicio"]
        data2=self.cleaned_data["FechaFin"]

        if data >data2:
             raise ValidationError({"FechaInicio": ("La fecha no puede ser menor que la fecha fin")})
       
    class Meta:
        model=ExperienciaLaboral
        fields=["Empresa","Puesto","FechaInicio","FechaFin"]
        labels={
            "FechaInicio": "Fecha de Inicio",
            "FechaFinFinal": "Fecha de Fin",
        }
        widgets={
            "Empresa":forms.TextInput(
                attrs={
                    "class": "m-2",

                }
            ),
            "Puesto":forms.TextInput(
                attrs={
                    "class": "m-2",

                }
            ),
            "FechaInicio":forms.DateInput(
                attrs={
                    "type":"date",
                    "class":"m-2",
                }
            ),
            "FechaFin":forms.DateInput(
                attrs={
                    "type":"date",
                    "class":"m-2",
                }
            ),
        }

class Moderador(forms.Form):
   
    Usuario=forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False, is_superuser=False))


class Administrador(forms.Form):
    Usuario=forms.ModelChoiceField(queryset=User.objects.filter( is_superuser=False))