from .models import CarroDeCompra

def carro_compras(request):
    if request.user.is_authenticated:
        carro, created = CarroDeCompra.objects.get_or_create(usuario=request.user)
        libros_en_carro = carro.librosAcomprar.all()
    else:
        libros_en_carro = []
    return {'libros_en_carro': libros_en_carro}