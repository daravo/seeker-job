from django.urls import re_path
from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("registro_empresa", views.empresa1, name="registro_empresa"),
    path("registro_empresa2/<str:pk>", views.empresa2, name="registro_empresa2"),
  
    path("registro_OfertaEmpleo",views.ofertaEmpleo, name="registro_OfertaEmpleo"),
    path("misOfertasDeEmpleo",views.misOfertasEmpleo.as_view(), name="misOfertasDeEmpleo"),
    path("detalleOfertaEmpleo/<str:pk>", views.OfertaEmpleoDetailView.as_view(), name="ofertaempleo-detail"),
    path("detalleOfertaEmpleo/<str:pk>/modificarOferta", views.OfertaEmpleoUpdate.as_view(), name="ofertaempleo-update"),
    path("registro_usuario", views.usuario1, name="registro_usuario"),
    path("registro_usuario2/<str:pk>", views.usuario2, name="registro_usuario2"),
    path("OfertasDeEmpleo",views.listaOfertaEmpleo.as_view(), name="OfertasDeEmpleo"),
    path("detalleOfertaEmpleo/<str:pk>/aplicar_candidato", views.aplicarCandidato, name="aplicar_candidato"),
    path("lista_empresas",views.listaEmpresas.as_view(), name="listadoEmpresas"),
    path("detalle_empresa/<str:pk>/", views.EmpresaPerfil.as_view(), name="empresa_detail"),
    path("lista_usuarios", views.listaUsuarios.as_view(), name="listadoUsuarios"),
    path("detalleUsuario/<str:pk>/", views.UsuarioPerfil.as_view(), name="usuario_detail"),
    path("detalle_empresa/<str:pk>/modificarEmpresa",views.actualizarEmpresa.as_view(), name="actualizarEmpresa"),
    path("detalleUsuario/<str:pk>/modificarUsuario",views.actualizarUsuario.as_view(), name="actualizarUsuario"),
    path("registro", views.registro, name="registro"),
    path("detalle_empresa/", views.MiPerfilEmpresa, name="miempresa_detail"),
    path("detalle_usuario/", views.MiPerfilUsuario, name="miusuario_detail"),
    path("buscador/", views.buscador, name="buscador"),
    path("api/mensajes/", views.CanalMensajeListApiView.as_view(), name="api-mensajes"),
    path("api/todosmensajes/", views.CanalTodosMensajesListApiView.as_view(), name="api-todosmensajes"),
    path("api/todosuser/", views.UsuariosListApiView.as_view(), name="api-todosuser"),
    path("detalleOfertaEmpleo/<str:pk>/cancelarcandidatura", views.cancelarCandidatura, name="cancelarCandidatura"),
    path("detalleOfertaEmpleo/<str:pk>/<str:pk2>/cancelarcandidatura", views.empresaCancelaCandidatura, name="empresa_cancelarCandidatura"),
    path("detalleUsuario/<str:pk>/AnadirTitulo", views.CreacionTitulos, name="creartitulo"),
    path("detalle_usuario/AnadirTitulo", views.CreacionTitulos, name="creartitulo"),
    path("detalle_titulo/<str:pk>/BorrarTitulo/", views.borrarTitulos, name="borrarTitulo"),
    path("detalle_titulo/<str:pk>/changeTitulo/", views.TituloUpdateView.as_view(), name="changeTitulo"),
    path("detalle_titulo/<str:pk>", views.TituloDetailView.as_view(), name="titulo_detail"),
    path("AñadirIdioma", views.creacionIdioma, name="crearIdioma"),
    path("detalle_idioma/<str:pk>", views.IdiomaDetailView.as_view(), name="idioma_detail"),
    path("detalle_idioma/<str:pk>/changeIdioma/", views.IdiomaUpdateView.as_view(), name="idioma_update"),
    path("detalle_idioma/<str:pk>/BorrarIdioma", views.IdiomaBorrado, name="borrarIdioma"),
    path("AñadirExperienciaLaboral", views.creacionExperienciaLaboral, name="crearExperienciaLaboral"),
    path("detalleExperiencia/<str:pk>", views.ExperienciaDetailView.as_view(), name="ExperienciaLaboral_detail"),
    path("detalleExperiencia/<str:pk>/changeExperiencia", views.ExperienciaUpdateView.as_view(), name="change_Experiencia"),
    path("detalleExperiencia/<str:pk>/BorrarExperiencia", views.BorrarExperiencia, name="BorrarExperiencia"),
    path("AñadirModerador", views.NuevoMod, name="nuevo_Mod"),
    path("detalleOfertaEmpleo/<str:pk>/borrarOferta", views.borrarOferta, name="borrarOfertaEmpleo"),
    path("detalleUsuario/<str:pk>/borrarUsuario", views.BorrarUsuario, name="borrarUsuario"),
    path("detalle_empresa/<str:pk>/borrarEmpresa", views.BorrarEmpresa, name="borrarEmpresa"),
    path("AñadirAdmin", views.NuevoAdmin, name="nuevoAdmin")
]

UUID_CANAL_REGEX =r"canal/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})"
UUID_CANAL_REGEX2 =r"canal/ajax/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})"

urlpatterns += [
    re_path(UUID_CANAL_REGEX, views.CanalDetailView.as_view()),
    path("chat/<str:username>", views.mensajes_privados),
    path("ms/<str:username>", views.DetailMs.as_view(), name="detailms"),
    re_path(UUID_CANAL_REGEX2, views.dameNumeroMensajes, name="mensajes"),
    path("inbox", views.inbox.as_view(), name="inbox"),

]
