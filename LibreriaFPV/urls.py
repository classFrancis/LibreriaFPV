"""
URL configuration for LibreriaFPV project.

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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from libreriaApp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfiladmin/', views.perfil_admin, name='perfiladmin'),
    path('catalogolibros/',views.catalogo, name='catalogolibros'),
    path('verlibro/<int:libro_id>/',views.ver_libro, name='verlibro'),
    path('carro/agregar/<int:libro_id>/', views.agregar_al_carro, name='agregar_al_carro'),
    path('carro/eliminar/<int:libro_id>', views.eliminar_del_carro, name='eliminar_del_carro'),
    path('eliminarunlibro/<int:libro_id>', views.eliminar_un_libro_del_carro,name='eliminar_un_libro'),
    path('carro/vaciar', views.vaciar_carro, name='vaciar_carro'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)