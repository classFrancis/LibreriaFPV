from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')

#Agregar un libro
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

#Listar libros del catalogo en el template del catalogo
def catalogo(request):
    libros = Libro.objects.all()
    return render(request, 'catalogo.html', {'libros': libros})

#Ver Libro del catalogo
def ver_libro(request):
    return render(request, 'libro.html')

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

#Cerrar sesion
def cerrar_sesion(request):
    logout(request)
    return redirect(reverse('login')+"?message=Has cerrado sesión correctamente.")


