from itertools import count
from pyexpat import model



from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from django.db.models import Count
from django.apps import apps
import datetime
# Create your models here.

class Empresa(models.Model):
    login=models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_empresa=models.CharField(max_length=100)
    telefono=models.CharField(max_length=15, blank=True)
    email=models.CharField(max_length=100, blank=True)
    Foto= models.ImageField("Imagen de Perfil", default="user-default.png")
    
    def __str__(self):
        return self.nombre_empresa

    def get_absolute_url(self):
        return reverse("empresa_detail", args=[str(self.id)])
    


class Usuario(models.Model):
    login=models.ForeignKey(User, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=70, blank=True)
    anioNacimiento=models.DateField(blank=True)
    Foto= models.ImageField("Imagen de Perfil", default="user-default.png")
    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("usuario_detail", args=[str(self.id)])

class Titulos(models.Model):
    Usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    InstitucionEducativa=models.CharField(max_length=150, blank=True)
    Titulo=models.CharField(max_length=70)
    FechaInicio=models.DateField()
    FechaFinFinal=models.DateField()
    def __str__(self):
        cadena=str(self.Usuario)+", "+self.Titulo
        return cadena

    def get_absolute_url(self):
        return reverse("titulo_detail", args=[str(self.id)])

class IdiomaNiveles(models.Model):
    nivel=models.CharField(max_length=25)
    def __str__(self):
        return self.nivel


class Idiomas(models.Model):
    Usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Idioma=models.CharField(max_length=25)
    nivel=models.ForeignKey(IdiomaNiveles, on_delete=models.CASCADE, default=1)
    def __str__(self):
        cadena=str(self.Usuario)+", "+self.Idioma+", "+ str(self.nivel)
        return cadena

    def get_absolute_url(self):
        return reverse("idioma_detail", args=[str(self.id)])

class ExperienciaLaboral(models.Model):
    Usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Empresa=models.CharField(max_length=75, blank=True)
    Puesto=models.CharField(max_length=70)
    FechaInicio=models.DateField()
    FechaFin=models.DateField()
    def __str__(self):
        cadena=str(self.Usuario)+", "+self.Puesto
        return cadena
    def get_absolute_url(self):
        return reverse("ExperienciaLaboral_detail", args=[str(self.id)])



    

    
    
    
class PuestoDeTrabajo(models.Model):
    puesto=models.CharField(max_length=50)

    def __str__(self):
        return self.puesto

class EstudiosMinimos(models.Model):
    estudios=models.CharField(max_length=60)

    def __str__(self):
        return self.estudios

class JornadaLaboral(models.Model):
    tipoJornada=models.CharField(max_length=40)
    def __str__(self):
        return self.tipoJornada

class TipoContrato(models.Model):
    contrato=models.CharField(max_length=30)
    def __str__(self):
        return self.contrato

class Presencialidad(models.Model):
    trabajo=models.CharField(max_length=30)
    def __str__(self):
        return self.trabajo

   

class OfertaEmpleo(models.Model):
    EmpresaSolicitante=models.ForeignKey(Empresa, on_delete=models.CASCADE)
    Titulo=models.CharField(max_length=30)
    Descripcion=models.CharField(max_length=100)
    UltimoDiaInscripcion=models.DateField(help_text= "Escriba una fecha posterior a una semana a partir del dia de hoy")
    Presencialidad=models.ForeignKey(Presencialidad,on_delete=models.CASCADE, default=1)
    Estudios=models.ForeignKey(EstudiosMinimos,on_delete=models.CASCADE, default=1)
    Jornada=models.ForeignKey(JornadaLaboral,on_delete=models.CASCADE, default=1)
    Puesto=models.ForeignKey(PuestoDeTrabajo,on_delete=models.CASCADE, default=1)
    Contrato=models.ForeignKey(TipoContrato,on_delete=models.CASCADE, default=1)


    @property
    def Inscripcion(self):
        return datetime.date.today() < self.UltimoDiaInscripcion

    def __str__(self):
        cadena1=self.EmpresaSolicitante.nombre_empresa
        cadena1=str(cadena1)
        cadena2=self.Titulo
        cadena2=str(cadena2)
        cadena3=cadena1+", "+cadena2
        return cadena3
    def get_absolute_url(self):
        return reverse("ofertaempleo-detail", args=[str(self.id)])
    Candidatos=models.ManyToManyField(Usuario, blank=True)
    class Meta:
        permissions =(("aplicar_como_candidato","aplicar_como_candidato"),)


class ModelBase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, editable=True)
    tiempo= models.DateTimeField(auto_now=True)
    actualizar=models.DateTimeField(auto_now=True)

    class Meta: 
        abstract= True
    
class CanalMensaje(ModelBase):
    canal= models.ForeignKey("Canal", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()

class CanalUsuario(ModelBase):
    canal= models.ForeignKey("Canal", null=True, on_delete=models.SET_NULL)
    usuario= models.ForeignKey(User, on_delete=models.CASCADE)

class CanalQuerySet(models.QuerySet):
    
    def solo_uno(self):
        return self.annotate(num_usuarios=Count("usuarios")).filter(num_usuarios=1)

    def solo_dos(self):
        return self.annotate(num_usuarios=Count("usuarios")).filter(num_usuarios=2)
    
    def filtrar_por_username(self, username):
        return self.filter(canalusuario__usuario__username=username)

class CanalManager(models.Manager):
    
    def get_queryset(self, *args, **kwargs):
        return CanalQuerySet(self.model, using=self._db)

    def filtrar_ms_por_privado(self, username_a, username_b):
        return self.get_queryset().solo_dos().filtrar_por_username(username_a).filtrar_por_username(username_b)
    
    def obtener_o_crear_canal_usuario_actual(self, user):
        qs= self.get_queryset().solo_uno().filtrar_por_username(user.username)
        if qs.exists():
            return qs.order_by("tiempo").first, False
            
        canal_obj= Canal.objects.create()
        CanalUsuario.objects.create(usuario=user, canal=canal_obj)
        return canal_obj, True

    def obtener_o_crear_canal_ms(self,username_a, username_b):
        qs= self.filtrar_ms_por_privado(username_a, username_b)
        if qs.exists():
            return qs.order_by("tiempo").first(), False
        
       
        
        User=apps.get_model("auth", model_name="User")
        usuario_a, usuario_b= None, None
        try: 
            usuario_a=User.objects.get(username=username_a)
        except User.DoesNotExist:
            return None, False

        try: 
            usuario_b=User.objects.get(username=username_b)
        except User.DoesNotExist:
            return None, False

        if usuario_a==None or usuario_b== None:
            return None, False
        obj_canal= Canal.objects.create()
        
        canal_usuario_a=CanalUsuario(usuario=usuario_a, canal=obj_canal)
        canal_usuario_b= CanalUsuario(usuario=usuario_b, canal=obj_canal)
        CanalUsuario.objects.bulk_create([canal_usuario_a, canal_usuario_b])
        return obj_canal, True


class Canal(ModelBase):
    usuarios= models.ManyToManyField(User, blank=True, through=CanalUsuario)

    objects=CanalManager()

