from .models import CarroDeCompra,ItemCarro
from django.db.models import Sum, F


def carro_compras(request):
    if request.user.is_authenticated:
        carro, created = CarroDeCompra.objects.get_or_create(usuario=request.user)
        items_en_carro = ItemCarro.objects.filter(carro=carro)
        total_precio = items_en_carro.annotate(total_item=F('libro__precio') * F('cantidad')).aggregate(Sum('total_item'))['total_item__sum'] or 0
    else:
        items_en_carro = []
        total_precio = 0
    return {'items_en_carro': items_en_carro, 'total_precio': total_precio}    