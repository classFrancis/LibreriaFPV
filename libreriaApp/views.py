
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
import random

# Create your views here.

#Render main page y muestra libros en el index
def index(request):
    cantidad_libros=6
    libros=list(Libro.objects.all())
    libros_aleatorios=random.sample(libros,min(cantidad_libros,len(libros)))
    return render(request,'index.html',{'libros':libros_aleatorios})

#Agregar un libro al sistema
@login_required
def add_libro(request):
    form=LibroRegistroForm()
    if request.method=='POST':
        form=LibroRegistroForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('agregar_libro_al_sistema')+'?messge=Registro exitoso.')
        else:
            return render(request,'agregarlibro.html',{'form':form})
    else:
        form=LibroRegistroForm()
    return render(request,'agregarlibro.html',{'form':form})

#Modificar libro del sistema
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

#Agregar libro al carro de compras como usuario registrado
@login_required
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
@login_required
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
@login_required
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
@login_required
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
def catalogo_edicion(request):
    libros = Libro.objects.all()
    return render(request, 'catalogoedicionlibro.html', {'libros': libros})

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
@login_required
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
@login_required
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
@login_required
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

#Render perfil super usuario
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


