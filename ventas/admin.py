from django.contrib import admin
from ventas.models import Clientes, Producto

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'id')
    search_fields = ['nombre']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filters = ()
    fieldsets = ()

admin.site.register(Clientes, ClienteAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'descripcion', 'precio', 'cantidad')
    search_fields = ['codigo']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filters = ()
    fieldsets = ()

admin.site.register(Producto, ProductoAdmin)

