
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import random

# Create your views here.

#Render main page y muestra libros en el index
def index(request):
    cantidad_libros=6
    libros=list(Libro.objects.all())
    libros_aleatorios=random.sample(libros,min(cantidad_libros,len(libros)))
    return render(request,'index.html',{'libros':libros_aleatorios})

#Agregar un libro al sistema
def add_libro(request):
    form=LibroRegistroForm()
    if request.method=='POST':
        form=LibroRegistroForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('TEMPLATE DE REGISTRO')+'?messge=Registro exitoso.')
        else:
            return render(request,'TEMPLATE DE REGISTRO',{'form':form})
    else:
        form=LibroRegistroForm()
    return render(request,'TEMPLATE DE REGISTRO',{'form':form})

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

#Render perfil usuario
@login_required(login_url='login')
def perfil(request):
    return render(request,'perfil.html')

#Render perfil super usuario
@login_required(login_url='login')
def perfil_admin(request):
    return render(request,'perfilAdmin.html')

#Login al sistema
def login_usuario(request):
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


