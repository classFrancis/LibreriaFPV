"""Aqui van los formularios que se renderizan en los templates a traves de las views, el uso del framework se encarga de las
validaciones de entrada de datos"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

#Login
class UsuarioLoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de Usuario'}),label="")
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),label="")

#Creacion de un usuario
class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model=Usuario
        fields=('first_name','last_name','email','rut','username')
    
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),label="")    
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellifo'}),label="")  
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),label="")  
    rut=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'rut'}),label="")
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de Usuario'}),label="")
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),label="")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar Password'}),label="")

    def save(self,commit=True):
        usuario=super().save(commit=False)
        if commit:
            usuario.save()
            perfil=Perfil(usuario=usuario)
            perfil.save()
        return usuario

#Registra un libro en el sistema 
class LibroRegistroForm(forms.ModelFormForm):
    class Meta:
        model = Libro
        fields = '__all__'

    idLibro=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID del Libro'}),label="")
    titulo=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),label="")
    autorlibro=forms.ModelChoiceField(queryset=Autor.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}),label="")
    editorial=forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Editorial'}),label="")
    edicion=forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Edición'}),label="")
    fechaDePublicacion=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),label="")
    cantidad=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),label="")
    precio=forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),label="")
    disponible=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),label="",required=False)
    imagen=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}),label="",required=False)

    def clean_imagen(self):
        imagen=self.cleaned_data.get('imagen', False)
        if imagen:
            if imagen.size > 1 * 1024 * 1024:
                raise forms.ValidationError("El archivo de imagen es demasiado grande ( > 1mb ).")
            return imagen

    def save(self,commit=True):
        libro=super(LibroRegistroForm, self).save(commit=False)
        if self.cleaned_data.get('imagen'):
            imagen=self.cleaned_data['imagen']
            libro.imagen = imagen.read()
        if commit:
            libro.save()
        return libro


