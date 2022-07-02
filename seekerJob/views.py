from ast import keyword
from distutils.log import Log
from multiprocessing import context, get_context
from pyexpat import model
from re import template
from django.shortcuts import render
from .models import Empresa, OfertaEmpleo, Usuario
from django.views import generic
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .models import CanalMensaje, CanalUsuario, Canal
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import FormMixin
from django.views.generic import View
from .filters import *
from django_filters.views import FilterView
from .models import *

# Create your views here.

def index(request):
    hola="hola primera pagina"
    return render(
        request,
        'index.html',
        context={'hola':hola},
    )


def empresa1(request):
    
   
    if request.method =="POST":
        form=RegistroUsuarioEmpresaForm(request.POST)
        if form.is_valid():
            user=form.cleaned_data["username"]
            print(user)
            print(type(user) is str)
            
            form.save()
            
            return redirect("registro_empresa2/"+user)
           
            
    else:
        
        form=RegistroUsuarioEmpresaForm
   
    return render(request, "seekerJob/empresa_form.html",{"form":form})

def empresa2(request, pk):
    usu=User.objects.get(username=pk)
    if request.method =="POST":
        form=RegistroEmpresaForm(request.POST)
        if form.is_valid():
            Empresa.objects.create(login=usu,
            nombre_empresa=form.cleaned_data["nombre_empresa"],
            telefono=form.cleaned_data["telefono"])
            grupoEmpresa =Group.objects.get(name="Empresas")
            usu.groups.add(grupoEmpresa)
           
            
            return redirect("index")
    else:
        form=RegistroEmpresaForm
    return render(request, "seekerJob/empresa_form.html",{"form":form})

@permission_required("seekerJob.add_ofertaempleo")
def ofertaEmpleo(request):
    if request.method=="POST":
        form=RegistroOfertaEmpleo(request.POST)
        empresa=Empresa.objects.get(login=request.user.id)
        if form.is_valid():
            OfertaEmpleo.objects.create(EmpresaSolicitante=empresa,
            Titulo=form.cleaned_data["Titulo"],
            Descripcion=form.cleaned_data["Descripcion"],
            UltimoDiaInscripcion=form.cleaned_data["UltimoDiaInscripcion"],
            Presencialidad=form.cleaned_data["Presencialidad"],
            Estudios=form.cleaned_data["Estudios"],
            Jornada=form.cleaned_data["Jornada"],
            Puesto=form.cleaned_data["Puesto"],
            Contrato=form.cleaned_data["Contrato"])
            return redirect("index")
    else:
        form=RegistroOfertaEmpleo
    return render(request, "seekerJob/ofertaEmpleo_form.html",{"form":form})

            
class misOfertasEmpleo(generic.ListView):
   
    model=OfertaEmpleo
    template_name="seekerJob/misOfertasEmpleo.html"
    paginate_by=10
    def get_queryset(self):
        
        
        return OfertaEmpleo.objects.filter(EmpresaSolicitante=Empresa.objects.get(login=self.request.user))

class OfertaEmpleoDetailView(generic.DetailView):
    model=OfertaEmpleo
    template_name="seekerJob/detalleOfertaEmpleo.html"

class OfertaEmpleoUpdate(UpdateView):
    model=OfertaEmpleo
    form_class=RegistroOfertaEmpleo
    template_name="seekerJob/ofertaEmpleo_form.html"
   

def usuario1(request):
    
    
    if request.method =="POST":
        form=RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user=form.cleaned_data["username"]
            print(user)
            print(type(user) is str)
            
            form.save()
            
            return redirect("registro_usuario2/"+user)
           
            
    else:
        form=RegistroUsuarioForm
    return render(request, "seekerJob/usuario_form.html",{"form":form})


def usuario2(request, pk):
    usu=User.objects.get(username=pk)
    if request.method =="POST":
        form=RegistroUsuario2Form(request.POST)
        if form.is_valid():
            Usuario.objects.create(login=usu,
            nombre=form.cleaned_data["nombre"],
            apellido=form.cleaned_data["apellido"],
            anioNacimiento=form.cleaned_data["anioNacimiento"]
            )
            grupoEmpresa =Group.objects.get(name="Usuarios")
            usu.groups.add(grupoEmpresa)
           
            
            return redirect("index")
    else:
        form=RegistroUsuario2Form
    return render(request, "seekerJob/usuario_form.html",{"form":form})

class listaOfertaEmpleo(LoginRequiredMixin,FilterView):
    model=OfertaEmpleo
    
    context_object_name="OfertaEmpleo_list"
    template_name="seekerJob/ofertaempleo_list.html"
    filterset_class=OfertaFilter

def aplicarCandidato(request, pk):
    
    usu=request.user
    oferta=OfertaEmpleo.objects.get(id=pk)
    oferta.Candidatos.add(Usuario.objects.get(login=usu))
    return redirect("/seekerJob/detalleOfertaEmpleo/"+pk)


@login_required
def mensajes_privados(request, username, *args, **kwargs):
    mi_username=request.user.username
    canal, created= Canal.objects.obtener_o_crear_canal_ms(mi_username, username)
    if created:
        print("Si fue creado")
    
       
    Usuarios_Canal= canal.canalusuario_set.all().values("usuario__username")
    print(Usuarios_Canal)
    mensaje_canal= canal.canalmensaje_set.all()
    print(mensaje_canal.values("texto"))
    
    return HttpResponse(f"Nuestro Canal - {canal.id}")



class CanalFormMixin(FormMixin):
    form_class=FormMensaje
    success_url= "./"

    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def get_success_url(self):
        return self.request.path

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        form = self.get_form()
        if form.is_valid():
            canal= self.get_object()
            usuario=self.request.user
            mensaje=form.cleaned_data.get("mensaje")
            canal_obj=CanalMensaje.objects.create(canal=canal, usuario=usuario, texto=mensaje)

            if self.is_ajax():
                return JsonResponse({"mensaje": canal_obj.texto,
                "username": canal_obj.usuario.username,

                }, status=201)
            return super().form_valid(form)
        else:
            if self.is_ajax():
                return JsonResponse({"Error": form.errors},status=400)
            return super().form_invalid(form)


class DetailMs(LoginRequiredMixin, CanalFormMixin,generic.DetailView):
    template_name= "seekerJob/canal_detail.html"
    def get_object(self, *args, **kwargs):
        mi_username= self.request.user.username
        username=self.kwargs.get("username")
        canal, _ = Canal.objects.obtener_o_crear_canal_ms(mi_username, username)

        if username== mi_username:
            mi_canal, _ =Canal.objects.obtener_o_crear_canal_usuario_actual(self.request.user)

            return mi_canal

        if canal==None:
            raise Http404

        return canal


class CanalDetailView(LoginRequiredMixin, CanalFormMixin,generic.DetailView):
    template="seekerJob/canal_detail.html"
    queryset=Canal.objects.all()
    
    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        
        obj= context["object"]
        print(obj)
        context["si_canal_miembro"]= self.request.user in obj.usuarios.all()
        return context
"""
        if self.request.user not in obj.usuarios.all():
            raise PermissionDenied
""" 


"""
    def get_queryset(self) :
        usuario=self.request.user
        username=usuario.username
        qs= Canal.objects.all().filtrar_por_username(username)
        return qs
"""

def dameNumeroMensajes(request, pk):

    
    qs=CanalMensaje.objects.all().filter(canal_id=pk)
    qs=len(qs)
    data={
        "mensajes": qs
    }
    return JsonResponse (data, safe=False)
    
class inbox(View):
    def get(self, request):
        inbox= Canal.objects.filter(canalusuario__usuario__in=[request.user.id])

        context={
            "inbox":inbox
        }
        return render(request, "seekerJob/inbox.html", context)

class listaEmpresas(LoginRequiredMixin,generic.ListView):
    model=Empresa
    paginate_by=5
    template_name="seekerJob/empresa_list.html"

class EmpresaPerfil(LoginRequiredMixin,generic.DetailView):
    model=Empresa
    template_name="seekerJob/empresa_detail.html"

    def get_context_data(self, **kwargs):
        empresa=Empresa.objects.get(id=self.kwargs["pk"])
        oferta=OfertaEmpleo.objects.filter(EmpresaSolicitante=Empresa.objects.get(id=self.kwargs["pk"]))
        context ={
            "empresa": empresa,
            "oferta":oferta
        }
        return context
       
class listaUsuarios(LoginRequiredMixin,generic.ListView):
    model=Usuario
    paginate_by=5
    template_name="seekerJob/usuario_list.html"

class UsuarioPerfil(LoginRequiredMixin,generic.DetailView):
    model=Usuario
    template_name="seekerJob/usuario_detail.html"
    def get_context_data(self, **kwargs):
        usuario=Usuario.objects.get(id=self.kwargs["pk"])
        titulos=Titulos.objects.filter(Usuario=usuario)
        idiomas=Idiomas.objects.filter(Usuario=usuario)
        experiencia=ExperienciaLaboral.objects.filter(Usuario=usuario)
        context={
            "titulos":titulos,
            "usuario":usuario,
            "idiomas":idiomas,
            "experiencia":experiencia,
        }
        return context
    
class actualizarEmpresa(LoginRequiredMixin,UpdateView):
    model=Empresa
    template_name="seekerJob/empresa_form.html"
    fields=("nombre_empresa","telefono","email", "Foto")

class actualizarUsuario(LoginRequiredMixin,UpdateView):
    model=Usuario
    template_name="seekerJob/usuario_form.html"
    fields=("nombre","apellido","anioNacimiento", "Foto")

def registro(request):
    
    return render(
        request,
        'registro.html',
        context={},
    )
@login_required
def MiPerfilEmpresa(request):
    empresa=Empresa.objects.get(login=request.user)
    oferta=OfertaEmpleo.objects.filter(EmpresaSolicitante=Empresa.objects.get(login=request.user))
   
    return render(request, "seekerJob/empresa_detail.html",{
            "empresa": empresa,
            "oferta":oferta})

@login_required
def MiPerfilUsuario(request):
    usuario=Usuario.objects.get(login=request.user)
    titulos=Titulos.objects.filter(Usuario=usuario)
    idiomas=Idiomas.objects.filter(Usuario=usuario)
    experiencia=ExperienciaLaboral.objects.filter(Usuario=usuario)
    
    return render(request, "seekerJob/usuario_detail.html",{
            "usuario": usuario, "titulos":titulos, "idiomas":idiomas, "experiencia":experiencia,

            })
from django.core.paginator import Paginator
from itertools import chain
def buscador(request):
    if request.method =="POST":
        resultado=request.POST["searched"]
        usuarios=Usuario.objects.filter(nombre__contains=resultado)
        
        ofertas=OfertaEmpleo.objects.filter(Titulo__contains=resultado)
        empresas=Empresa.objects.filter(nombre_empresa__contains=resultado)
        total=list(chain(usuarios, ofertas, empresas))
        print(total)
        paginator=Paginator(total,5)
        page_number=request.GET.get("page")
        page_obj=paginator.get_page(page_number)
        return render(request, "seekerJob/buscador.html",{"resultado":resultado, "usuarios":usuarios,
        "ofertas":ofertas, "empresas":empresas, "page_obj":page_obj})

    else:
        return render(request, "seekerJob/buscador.html",{})


from rest_framework.generics import ListAPIView
from .serializers import *

class CanalMensajeListApiView(ListAPIView):
    serializer_class=CanalMensajeSerializer
    def get_queryset(self):
        kword=self.request.query_params.get("kword","")
        print(kword)
        prueba=CanalMensaje.objects.filter(canal=kword)
        print(prueba)
        return prueba

class CanalTodosMensajesListApiView(ListAPIView):
    serializer_class=CanalMensajeSerializer
    def get_queryset(self):
        return CanalMensaje.objects.all() 
    
class UsuariosListApiView(ListAPIView):
    serializer_class=UsuariosSerializer
    def get_queryset(self):
        kword=self.request.query_params.get("kword","")
        print(kword)
        prueba=User.objects.filter(id=kword)
        print(prueba)
        return prueba

def cancelarCandidatura(request, pk):
    usu=request.user
    oferta=OfertaEmpleo.objects.get(id=pk)
    
    oferta.Candidatos.remove(Usuario.objects.get(login=usu))
    return redirect("/seekerJob/detalleOfertaEmpleo/"+pk)

def empresaCancelaCandidatura(request, pk, pk2):
    usu=User.objects.get(id=pk2)
    oferta=OfertaEmpleo.objects.get(id=pk)
    oferta.Candidatos.remove(Usuario.objects.get(login=usu))
    return redirect("/seekerJob/detalleOfertaEmpleo/"+pk)

def CreacionTitulos(request):
    form=FormTitulos(request.POST or None)
    error=""
    if request.method=="POST" and form.is_valid():
        
        usu=User.objects.get(id=request.user.id)
        usuario=Usuario.objects.get(login=usu)
        Titulos.objects.create(Usuario=usuario,
        InstitucionEducativa=form.cleaned_data["InstitucionEducativa"],
        Titulo=form.cleaned_data["Titulo"],
        FechaInicio=form.cleaned_data["FechaInicio"],
        FechaFinFinal=form.cleaned_data["FechaFinFinal"])
        return redirect(usuario.get_absolute_url())
    elif request.method=="GET":
        form=FormTitulos
        
    else:
        error= "La fecha de Inicio tiene que ser anterior que la fecha fin"
        form=FormTitulos
    return render(request, "seekerJob/titulo.html",{"form":form, "error":error})



def borrarTitulos(request, pk):
    Titulos.objects.filter(id=pk).delete()
    return redirect("miusuario_detail")


class TituloDetailView(generic.DetailView):
    model=Titulos
    template_name="seekerJob/titulo_detail.html"

class TituloUpdateView(UpdateView):
    model=Titulos
    template_name="seekerJob/titulo_form.html"
    form_class=FormTitulos
    def get_success_url(self):
        return reverse("miusuario_detail")

def creacionIdioma(request):
    form=FormIdioma(request.POST or None)
    if request.method=="POST" and form.is_valid():
        usu=User.objects.get(id=request.user.id)
        usuario=Usuario.objects.get(login=usu)
        Idiomas.objects.create(Usuario=usuario,
        Idioma=form.cleaned_data["Idioma"],
        nivel=form.cleaned_data["nivel"])
        return redirect(usuario.get_absolute_url())
    else:
        form=FormIdioma
    return render(request, "seekerJob/idioma_form.html",{"form":form, })

class IdiomaDetailView(generic.DetailView):
    model=Idiomas
    template_name="seekerJob/idioma_detail.html"

class IdiomaUpdateView(UpdateView):
    model=Idiomas
    template_name="seekerJob/idioma_form.html"
    form_class=FormIdioma
    def get_success_url(self) :
        return reverse("miusuario_detail")

def IdiomaBorrado(request, pk):
    
    Idiomas.objects.filter(id=pk).delete()
    return redirect("miusuario_detail")

def creacionExperienciaLaboral(request):
    form=FormExperienciaLaboral(request.POST or None)
    error=""
    if request.method=="POST" and form.is_valid():
        usu=User.objects.get(id=request.user.id)
        usuario=Usuario.objects.get(login=usu)
        ExperienciaLaboral.objects.create(Usuario=usuario,
        Empresa=form.cleaned_data["Empresa"],
        Puesto=form.cleaned_data["Puesto"],
        FechaInicio=form.cleaned_data["FechaInicio"],
        FechaFin=form.cleaned_data["FechaFin"])
        return redirect(usuario.get_absolute_url())
    elif request.method=="GET":
        form=FormExperienciaLaboral
        
    else:
        error= "La fecha de Inicio tiene que ser anterior que la fecha fin"
        form=FormExperienciaLaboral
    return render(request, "seekerJob/ExperienciaLaboral_form.html",{"form":form, "error":error})

class ExperienciaDetailView(generic.DetailView):
    model=ExperienciaLaboral
    template_name="seekerJob/ExperienciaLaboral_detail.html"

class ExperienciaUpdateView(UpdateView):
    model=ExperienciaLaboral
    template_name="seekerJob/ExperienciaLaboral_form.html"
    form_class=FormExperienciaLaboral
    def get_success_url(self) :
        return reverse("miusuario_detail")

def BorrarExperiencia(request, pk):
    ExperienciaLaboral.objects.filter(id=pk).delete()
    return redirect("miusuario_detail")

def NuevoMod(request):
    form=Moderador(request.POST or None)
    mensaje=""
    if request.method=="POST" and form.is_valid():
       usu=form.cleaned_data["Usuario"]
       grupoMod=Group.objects.get(name="Moderadores")
       usu.groups.add(grupoMod)
       usu.is_staff=True
       usu.save()
       
       mensaje="El Usuario se añadio al grupo de moderadores"


    return render(request, "seekerJob/Moderadores_form.html", {"form":form, "mensaje":mensaje})


def borrarOferta(request, pk):
    OfertaEmpleo.objects.filter(id=pk).delete()
    return redirect("OfertasDeEmpleo")

def BorrarUsuario(request, pk):
    usu=User.objects.filter(usuario__id=pk).delete()
    return redirect("listadoUsuarios")

def BorrarEmpresa(request, pk):
    User.objects.filter(empresa__id=pk).delete()
    return redirect("listadoEmpresas")

def NuevoAdmin(request):
    form=Administrador(request.POST or None)
    mensaje=""
    if request.method=="POST" and form.is_valid():
       usu=form.cleaned_data["Usuario"]
       grupoAdmin=Group.objects.get(name="Administradores")
       usu.groups.add(grupoAdmin)
       usu.is_staff=True
       usu.save()
       
       mensaje="El Usuario se añadio al grupo de administrador"


    return render(request, "seekerJob/Moderadores_form.html", {"form":form, "mensaje":mensaje})

