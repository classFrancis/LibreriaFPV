
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
import random
from django.db.models import Q 

#Decorador personalizado para verificar si el user es administrador
def es_admin(user):
    return user.is_active and user.is_superuser
admin_only = user_passes_test(es_admin, login_url='login')

#Render main page y muestra libros en el index
def index(request):
    cantidad_libros=6
    libros=list(Libro.objects.all())
    libros_aleatorios=random.sample(libros,min(cantidad_libros,len(libros)))
    return render(request,'index.html',{'libros':libros_aleatorios})

#Agregar un libro al sistema
@admin_only
@login_required(login_url='login')
def add_libro(request):
    form=LibroRegistroForm()
    if request.method=='POST':
        form=LibroRegistroForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('perfiladmin')+'?messge=Registro exitoso.')
        else:
            return render(request,'agregarlibro.html',{'form':form})
    else:
        form=LibroRegistroForm()
    return render(request,'agregarlibro.html',{'form':form})

#Agregar autor
@admin_only
@login_required(login_url='login')
def add_autor(request):
    form=AutorRegistroForm()
    if request.method=='POST':
        form=AutorRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('perfiladmin'))
        else:
            return render(request,'registrarautor.html',{'form':form})
    else:
        form=AutorRegistroForm()
    return render(request,'registrarautor.html',{'form':form})

#Modificar libro del sistema
@admin_only
def editar_libro(request,libro_id):
    libro=get_object_or_404(Libro,pk=libro_id)
    if request.method=='POST':
        form=LibroRegistroForm(request.POST,request.FILES,instance=libro)
        if form.is_valid():
            form.save()
            return redirect(reverse('catalogolibroseditar'))
    else:
        form=LibroRegistroForm(instance=libro)
    return render(request, 'editarlibro.html',{'form': form,'libro': libro})

#Editar autor
@admin_only
def editar_autor(request,autor_id):
    autor=get_object_or_404(Autor,pk=autor_id)
    if request.method=='POST':
        form=AutorRegistroForm(request.POST,instance=autor)
        if form.is_valid():
            form.save()
            return redirect(reverse('lista_editar_autor'))
    else:
        form=AutorRegistroForm(instance=autor)
    return render(request, 'modificarautor.html',{'form': form,'autor': autor})

#Listar usuarios
@admin_only
def lista_usuarios(request):
    usuarios=Usuario.objects.all()
    return render(request,'listausuarios.html',{'usuarios':usuarios})

#Listar autores
@admin_only
def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'listaautores.html', {'autores': autores})

#Listar autores eliminar
@admin_only
def lista_autores_eliminar(request):
    autores = Autor.objects.all()
    return render(request, 'listaautoreseliminar.html', {'autores': autores})

#Eliminar libro del sistema
@admin_only
def eliminar_libro(request,libro_id):
    libro=get_object_or_404(Libro,pk=libro_id)
    if request.method=='POST':
        libro.delete()
        return redirect(reverse('catalogo_libros_eliminar'))
    return render(request, 'eliminarlibro.html',{'libro':libro})

#Eliminar autor del sistema
@admin_only
def eliminar_autor(request,autor_id):
    autor=get_object_or_404(Autor,pk=autor_id)
    if request.method=='POST':
        autor.delete()
        return redirect(reverse('lista_eliminar_autor'))
    return render(request,'eliminarautor.html',{'autor':autor})

#Agregar libro al carro de compras como usuario registrado
@login_required(login_url='login')
@require_POST
def agregar_al_carro(request, libro_id):
    libro=get_object_or_404(Libro,id=libro_id)
    carro,created=CarroDeCompra.objects.get_or_create(usuario=request.user)
    item,created=ItemCarro.objects.get_or_create(carro=carro,libro=libro)
    if not created:
        item.cantidad+=1
        item.save()
    referrer_url = request.META.get('HTTP_REFERER')
    if 'verlibro' in referrer_url:
        return redirect('verlibro', libro_id=libro_id)
    else:
        return redirect('catalogolibros')

#Eliminar solo un libro del carro de compras como usuario registrado
@login_required(login_url='login')
@require_POST
def eliminar_un_libro_del_carro(request,libro_id):
    libro=get_object_or_404(Libro,id=libro_id)
    carro=get_object_or_404(CarroDeCompra,usuario=request.user)
    item=get_object_or_404(ItemCarro,carro=carro,libro=libro)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    referrer_url = request.META.get('HTTP_REFERER', 'catalogolibros')
    return redirect(referrer_url)    

#Eliminar libro del carro de compras como usuario registrado
@login_required(login_url='login')
@require_POST
def eliminar_del_carro(request, libro_id):
    libro=get_object_or_404(Libro, id=libro_id)
    carro=get_object_or_404(CarroDeCompra,usuario=request.user)
    carro.librosAcomprar.remove(libro)
    referrer_url = request.META.get('HTTP_REFERER')
    if 'verlibro' in referrer_url:
        return redirect('verlibro', libro_id=libro_id)
    else:
        return redirect('catalogolibros')

#Vaciar carro de compras como usuario registrado
@login_required(login_url='login')
@require_POST
def vaciar_carro(request):
    carro = get_object_or_404(CarroDeCompra, usuario=request.user)
    carro.librosAcomprar.clear() 
    carro.totalPrecio = 0.00  
    carro.save()
    return redirect('catalogolibros')

#Listar libros del catalogo en el template del catalogo
def catalogo(request):
    libros = Libro.objects.all()
    return render(request, 'catalogo.html', {'libros': libros})

#Listar libros del catalogo para editar
@admin_only
def catalogo_edicion(request):
    libros = Libro.objects.all()
    return render(request, 'catalogoedicionlibro.html', {'libros': libros})

#Listar libros del catalogo para eliminar
@admin_only
def catalogo_eliminacion_libro(request):
    libros = Libro.objects.all()
    return render(request, 'catalogoeliminarlibro.html', {'libros': libros})

#Ver Libro del catalogo
def ver_libro(request, libro_id):
    libro=get_object_or_404(Libro, pk=libro_id)
    return render(request, 'libro.html', {'libro':libro})

#Registrarse como usuario                 
def registrarse(request):
    form=UsuarioRegistroForm()
    if request.method=='POST':
        form=UsuarioRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form=UsuarioRegistroForm()           
    return render(request,'registrarse.html',{'form':form})

#Modificar password
@login_required(login_url='login')
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor, corrija el error.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiarpassword.html', {'form': form})

#Modificar datos de cuenta de usuario
@login_required(login_url='login')
def modificar_datos_cuenta(request):
    usuario=request.user
    if request.method=='POST':
        form=CustomUserChangeForm(request.POST,instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form=CustomUserChangeForm(instance=usuario)
    return render(request, 'modificardatosdecuenta.html',{'form':form})

#Registro y modificacion de datos de perfil de usuario
@login_required(login_url='login')
def registro_perfil(request):
    try:
        perfil,created=Perfil.objects.get_or_create(usuario=request.user)
        if request.method=='POST':
            form=PerfilRegistroForm(request.POST,request.FILES,instance=perfil)
            if form.is_valid():
                form.save()
                return redirect('perfil')
        else:
            form=PerfilRegistroForm(instance=perfil)
    except Perfil.DoesNotExist:
        form=PerfilRegistroForm()
    return render(request,'registroperfil.html',{'form':form})

#Render perfil usuario con datos de los mismos
@login_required(login_url='login')
def perfil(request):
    perfil_usuario, created = Perfil.objects.get_or_create(usuario=request.user)
    context = {'perfil': perfil_usuario,'usuario':request.user}
    return render(request,'perfil.html',context)

#Ver perfil como admin
@admin_only
def ver_perfil_como_admin(request, perfil_id):
    perfil=get_object_or_404(Perfil, pk=perfil_id)
    usuario=perfil.usuario
    return render(request, 'verperfilcomoadmin.html', {'perfil':perfil,'usuario':usuario})

#Render perfil super usuario
@admin_only
@login_required(login_url='login')
def perfil_admin(request):
    return render(request,'perfilAdmin.html')

#Login al sistema
def login_usuario(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('perfiladmin')
        else:
            return redirect('perfil')
        
    user_message=request.GET.get('message',None)  
    if request.method=="POST":
        form=UsuarioLoginForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
                if user.is_superuser:
                    return redirect('perfiladmin')
                else:
                    return redirect('perfil')
            else:
                user_message="Usuario o contraseña incorrectos."
        else:
            user_message="Por favor, ingrese un usuario y contraseña válidos."
            
    else:
        form=UsuarioLoginForm()
        
    return render(request,'login.html',{'form':form,'user_message':user_message})

#Cerrar sesion de usuario
def cerrar_sesion(request):
    logout(request)
    return redirect(reverse('login')+"?message=Has cerrado sesión correctamente.")

#Banear usuario
@admin_only
def banear_usuario(request,perfil_id):
    perfil=get_object_or_404(Perfil, pk=perfil_id)
    usuario=perfil.usuario
    usuario.is_active=not usuario.is_active
    usuario.save()
    return redirect('lista_usuarios')

#Buscar libro por nombre, autor o tematica
def buscar_libro(request):
    query=request.GET.get('q', '')  
    if query:
        libros=Libro.objects.filter(
            Q(titulo__icontains=query) | 
            Q(autorlibro__nombreAutor__icontains=query) | 
            Q(autorlibro__apellidoAutor__icontains=query) |
            Q(tematica__icontains=query) 
        )
    else:
        libros=Libro.objects.all()
    return render(request, 'resultadosdebusqueda.html', {'libros': libros})

#Buscar autor
def buscar_autor(request):
    query=request.GET.get('q','')
    if query:
        autores=Autor.objects.filter(
            Q(nombreAutor__icontains=query) |
            Q(apellidoAutor__icontains=query) 
        )
    else:
        autores=Autor.objects.all()
    return render(request,'resultadobusquedaautores.html',{'autores':autores})