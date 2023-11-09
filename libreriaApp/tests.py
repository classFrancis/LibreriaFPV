from django.test import TestCase, Client
from .forms import *
from .models import *
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

#Esto es un test para probar si el formulario de registro de Autores funciona
class AutorFormTestCase(TestCase):

    def test_autor_registro_form(self):

        autor_data={
            'nombreAutor':'autest',
            'apellidoAutor':'simba',
            'biografiaAutor':'El resultado de la prueba indica que la validación del formulario falló porque el campo biografiaAutor es obligatorio y no se ha proporcionado un valor válido. Aunque se ha suministrado un espacio en blanco ' ' como valor para biografiaAutor, esto no parece ser suficiente para pasar la validación, lo que sugiere que tu modelo o formulario requiere que ese campo tenga un contenido más significativo que un simple espacio. Para solucionar este fallo, necesitas proporcionar un valor no vacío para el campo biografiaAutor en tus datos de prueba. Asegúrate de que el valor que proporciones cumpla con las validaciones establecidas en tu modelo Autor. Por ejemplo, si se espera una biografía no vacía, deberías suministrar una cadena con texto real. Aquí está el código ajustado con un valor para biografiaAutor:'
        }

        form=AutorRegistroForm(data=autor_data)
        self.assertTrue(form.is_valid(),msg=form.errors)

        autor=form.save()
        self.assertIsNotNone(autor.id, 'El autor no se guardo en la base de datos')

#Esto es un test para probar si el formulario de registro de Libros funciona
class LibroFormTestCase(TestCase):

    def setUp(self):
        Autor.objects.create(nombreAutor='autest',apellidoAutor='simba',biografiaAutor='')

    def test_libro_form(self):
        autor = Autor.objects.first()
        
        libro_data = {
            'titulo': 'Prueba de libro',
            'autorlibro': autor.id,
            'tematica': 'Crimen',
            'editorial': 'Editorial Prueba',
            'edicion': '1',
            'fechaDePublicacion': '2023-01-01',
            'cantidad': 5,
            'precio': '19.99',
            'disponible': True,
        }
        
        form = LibroRegistroForm(data=libro_data)
        self.assertTrue(form.is_valid(),msg=form.errors)

        # Guarda el libro y verifica que se creó
        libro = form.save()
        self.assertIsNotNone(libro.id, "El libro no se guardó en la base de datos")

