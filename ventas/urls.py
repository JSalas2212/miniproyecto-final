from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.ventas_view, name='Productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    path('productos/pdf', views.generar_pdf, name='generar_pdf'),

    path('clientes/', views.clientes_view, name='Clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    # Rutas del carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('realizar_compra/', views.realizar_compra, name='realizar_compra'),
    path('ventas/pdf/', views.generar_pdf_ventas, name='generar_pdf_ventas'),
]
