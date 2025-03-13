from django.db import models

# Create your models here.

class Clientes(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='cliente'
        verbose_name_plural='clientes'
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, unique=True)
    precio = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='producto'
        verbose_name_plural='productos'
        order_with_respect_to = 'nombre'
    def __str__(self):
        return self.nombre
    
class Venta(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    total = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    fecha_venta = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'

    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre}"