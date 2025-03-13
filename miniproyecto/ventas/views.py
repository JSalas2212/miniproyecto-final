from django.shortcuts import render
from .models import Clientes, Producto

# Create your views here.

def ventas_view(request):
    productos = Producto.objects.all()
    context = {
        'productos': productos,
    }
    return render(request, 'ventas.html', context)

def clientes_view(request):
    clientes = Clientes.objects.all()
    context = {
        'clientes': clientes,
    }
    return render(request, 'clientes.html', context)