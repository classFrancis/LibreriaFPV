
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
    return render(request,'perfil.html',{'perfil': perfil_usuario,'usuario':request.user,'en_perfil': True})

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
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    return render(request,'perfilAdmin.html',{'notificaciones': notificaciones,'en_perfil': True})

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

#------------------------------------------------------------------------------------------------------------------------
#Crear publicacion con titulo y libro asociado
@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            nuevo_post = form.save(commit=False)
            nuevo_post.usuario = request.user  
            nuevo_post.save()
            messages.success(request, 'El post ha sido creado exitosamente.')
            return redirect('publicacion') 
        else:
            messages.error(request, 'Ha ocurrido un error al crear el post.')
    else:
        form = PostForm()

    return render(request, 'publicacion.html', {'form': form})

#Ver y gestionar posts and comentarios
@login_required
def publicacion(request):
    current_usuario = get_object_or_404(Usuario, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            posteo = form.save(commit=False)
            posteo.usuario = current_usuario
            posteo.save()
            return redirect('publicacion')
        else:
            # Aquí pasamos el formulario con errores de nuevo al template
            publicaciones = Post.objects.all()
            comentarios = Comentario.objects.all()
            form_comentario = ComentarioForm()
            return render(request, 'foro.html', {
                'form': form, 
                'publicaciones': publicaciones, 
                'comentarios': comentarios, 
                'form_comentario': form_comentario,
                'en_foro': True
            })
    else:
        form = PostForm()
        publicaciones = Post.objects.all()
        comentarios = Comentario.objects.all()
        form_comentario = ComentarioForm()
        return render(request, 'foro.html', {
            'form': form, 
            'publicaciones': publicaciones, 
            'comentarios': comentarios, 
            'form_comentario': form_comentario,
            'en_foro': True
        })

#crear comentario
@login_required
def comentar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Post, id=publicacion_id)
    form_comentario = ComentarioForm(request.POST)
    if form_comentario.is_valid():
        comentario = form_comentario.save(commit=False)
        comentario.usuario = request.user
        comentario.post = publicacion
        comentario.save()
        return redirect('publicacion')
    else:
        form_comentario = ComentarioForm()
        pass

#Eiminar publicacion
@login_required
def eliminar_publicacion(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.usuario == request.user or request.user.is_superuser:
        post.delete()
    return redirect('publicacion')

#Eliminar comentario
@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.usuario == request.user or request.user.is_superuser:
        comentario.delete()
    return redirect('publicacion')

#Editar publicacion
@login_required
def editar_publicacion(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.usuario != request.user:
        # Redireccionar o mostrar mensaje de error si el usuario no es el dueño de la publicación
        return redirect('publicacion')
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('publicacion')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'editarPublicacion.html', {'form': form})

#Editar comentario
@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if comentario.usuario != request.user:
        return redirect('publicacion')

    if request.method == "POST":
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('publicacion')
        else:
            # Imprimir los errores en la consola para depuración
            print(form.errors)
            # Pasar el formulario con errores a la plantilla
            return render(request, 'editarComentario.html', {'form': form})
    else:
        form = ComentarioForm(instance=comentario)
    
    return render(request, 'editarComentario.html', {'form': form})

#Crear reporte asociado a post y usuario
def crear_reporte(request, post_id=None):
    usuario_reportante = request.user
    post = get_object_or_404(Post, pk=post_id) if post_id else None

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = usuario_reportante
            reporte.post = post
            reporte.save()

            # Enviar notificaciones a todos los administradores
            # Utiliza tu modelo personalizado Usuario
            administradores = Usuario.objects.filter(is_superuser=True)
            for admin in administradores:
                notificacion = Notificacion(
                    usuario=admin,
                    post=reporte.post,
                    tipoNotificacion='REPORTE',
                    mensajeNotificacion=f'Titulo Post: {reporte.post.tituloPost}'
                )
                notificacion.save()

            return redirect('publicacion')
    else:
        form = ReporteForm()

    return render(request, 'reporteform.html', {'form': form, 'post': post})

#Crear reporte asociado a comentarioy usuario
def crear_reporte_comentario(request, comentario_id=None):
    usuario_reportante = request.user

    if comentario_id:
        comentario = get_object_or_404(Comentario, pk=comentario_id)
    else:
        # Si no hay comentario_id, posiblemente quieras redirigir o manejar este caso.
        return redirect('alguna_url_para_manejar_este_caso')

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = usuario_reportante
            reporte.comentario = comentario
            reporte.save()

            administradores = Usuario.objects.filter(is_superuser=True)
            for admin in administradores:
                notificacion = Notificacion(
                    usuario=admin,
                    comentario=comentario,  # Asegúrate de asignar el comentario aquí
                    tipoNotificacion='REPORTE',
                    mensajeNotificacion=f'Comentario: {reporte.comentario.contenidoComentario}'
                )
                notificacion.save()

            return redirect('publicacion')
    else:
        form = ReporteForm()

    return render(request, 'reporteformcomentario.html', {'form': form, 'comentario': comentario})


#Ver lista de reportes
@login_required
def listar_reportes(request):
    reportes = Reporte.objects.all()
    return render(request, 'listadereportes.html', {'reportes': reportes})

#Detalle reporte
@login_required
def detalle_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)

    # Formulario para cambiar el estado del reporte
    if request.method == 'POST':
        form = CambiarEstadoReporteForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            messages.success(request, "Estado del reporte actualizado")
            return redirect('detalle_reporte', reporte_id=reporte_id)
    else:
        form = CambiarEstadoReporteForm(instance=reporte)

    contexto = {
        'reporte': reporte,
        'form': form,
    }
    return render(request, 'detallereporte.html', contexto)

#Detalle notificaciones
@login_required
def detalle_notificacion(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, pk=notificacion_id)
    reporte = None
    if notificacion.post:
        reporte = Reporte.objects.filter(post=notificacion.post).first()
    elif notificacion.comentario:
        reporte = Reporte.objects.filter(comentario=notificacion.comentario).first()

    if reporte:
        if request.method == 'POST':
            form = CambiarEstadoReporteForm(request.POST, instance=reporte)
            if form.is_valid():
                form.save()
                messages.success(request, "Estado del reporte actualizado")
                return redirect('detalle_reporte', reporte_id=reporte.id)
        else:
            form = CambiarEstadoReporteForm(instance=reporte)
    else:
        form = None  # No hay reporte relacionado

    contexto = {
        'notificacion': notificacion,
        'form': form,
        'reporte': reporte
    }
    return render(request, 'detallereporte.html', contexto)

#puntuar publicacion
@login_required
def puntuar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    try:
        puntuacion_usuario = Puntuacion.objects.get(usuario=request.user, post=post)
    except Puntuacion.DoesNotExist:
        puntuacion_usuario = None

    if request.method == 'POST':
        form = PuntuarPostForm(request.POST, instance=puntuacion_usuario)
        if form.is_valid():
            puntuacion_usuario = form.save(commit=False)
            puntuacion_usuario.usuario = request.user
            puntuacion_usuario.post = post
            puntuacion_usuario.save()

            # Actualizar la puntuación promedio del post
            puntuacion_promedio = post.puntuaciones.aggregate(models.Avg('puntuacion'))['puntuacion__avg']
            post.puntuacion = puntuacion_promedio
            post.save()
            return redirect('publicacion')
    else:
        if puntuacion_usuario is not None:
            form = PuntuarPostForm(instance=puntuacion_usuario)
        else:
            form = PuntuarPostForm()

    return render(request, 'puntuarPost.html', {'form': form, 'post': post})