"""URL configuration for LibreriaFPV project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))"""
from django.contrib import admin
from django.urls import path
from libreriaApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('modificardatosdecuenta/',views.modificar_datos_cuenta,name='modificar_datos_de_cuenta'),
    path('campisarpassword/',views.cambiar_password,name='modificar_password'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('registroperfil/',views.registro_perfil,name='registro_perfil'),
    path('perfiladmin/', views.perfil_admin, name='perfiladmin'),
    path('catalogolibros/',views.catalogo, name='catalogolibros'),
    path('verlibro/<int:libro_id>/',views.ver_libro, name='verlibro'),
    path('carro/agregar/<int:libro_id>/', views.agregar_al_carro, name='agregar_al_carro'),
    path('carro/eliminar/<int:libro_id>', views.eliminar_del_carro, name='eliminar_del_carro'),
    path('eliminarunlibro/<int:libro_id>', views.eliminar_un_libro_del_carro,name='eliminar_un_libro'),
    path('carro/vaciar', views.vaciar_carro, name='vaciar_carro'),
    path('agregarlibro/',views.add_libro,name='agregar_libro_al_sistema'),
    path('catalogolibrosedicion/',views.catalogo_edicion, name='catalogolibroseditar'),
    path('editarlibro/<int:libro_id>',views.editar_libro,name='editar_libro_del_sistema'),
    path('catalogolibroseliminar/',views.catalogo_eliminacion_libro, name='catalogo_libros_eliminar'),
    path('eliminarlibro/<int:libro_id>',views.eliminar_libro,name='eliminar_libro_del_sistema'),
    path('registrarautor',views.add_autor,name='registrar_autor'),
    path('listaeditarautor/',views.lista_autores,name='lista_editar_autor'),
    path('editarautor/<int:autor_id>',views.editar_autor,name='editar_autor'),
    path('listaeditarautoreseliminar/',views.lista_autores_eliminar,name='lista_eliminar_autor'),
    path('eliminarautor/<int:autor_id>',views.eliminar_autor,name='eliminar_autor'),
    path('listarusuarios/',views.lista_usuarios,name='lista_usuarios'),
    path('verperfilcomoadmin/<int:perfil_id>',views.ver_perfil_como_admin,name='ver_perfil_como_admin'),
    path('banearusuario/<int:perfil_id>',views.banear_usuario,name='banear_usuario'),
    path('buscar_libro/', views.buscar_libro, name='buscar_libro'),
    path('autor_libro/', views.buscar_autor, name='buscar_autor'),
    #------------------------------------------------------------------
    path('crear_post/', views.crear_post, name='crear_post'),
    path('foro/', views.publicacion, name='publicacion'),
    path('foro/<int:publicacion_id>/', views.comentar_publicacion, name='comentarPublicacion'),
    path('eliminar_publicacion/<int:post_id>/', views.eliminar_publicacion, name='eliminarPublicacion'),
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminarComentario'),
    path('editar_publicacion/<int:post_id>/', views.editar_publicacion, name='editarPublicacion'),
    path('editar_comentario/<int:comentario_id>/', views.editar_comentario, name='editarComentario'),
    path('reportar/post/<int:post_id>/', views.crear_reporte, name='reportar_post'),
    path('reportar/comentario/<int:comentario_id>/', views.crear_reporte_comentario, name='reportar_comentario'),
    path('reportes/', views.listar_reportes, name='listar_reportes'),
    path('reportes/<int:reporte_id>/', views.detalle_reporte, name='detalle_reporte'),
    path('notificaciones/<int:notificacion_id>/', views.detalle_notificacion, name='detalle_notificacion'),
    path('puntuarPost/<int:post_id>/', views.puntuar_post, name='puntuar_post'),





]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)