from .models import CarroDeCompra
from django.db.models import Sum

def carro_compras(request):
    if request.user.is_authenticated:
        carro, created = CarroDeCompra.objects.get_or_create(usuario=request.user)
        libros_en_carro = carro.librosAcomprar.all()
        total_precio = libros_en_carro.aggregate(Sum('precio'))['precio__sum'] or 0
    else:
        libros_en_carro = []
        total_precio = 0
    return {'libros_en_carro': libros_en_carro,'total_precio': total_precio,}