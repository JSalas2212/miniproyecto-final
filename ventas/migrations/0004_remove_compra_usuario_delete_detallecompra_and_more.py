# Generated by Django 5.1.6 on 2025-02-23 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_detallecompra_compra'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='DetalleCompra',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='producto',
        ),
        migrations.DeleteModel(
            name='Compra',
        ),
        migrations.DeleteModel(
            name='Venta',
        ),
    ]
