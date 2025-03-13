from django.shortcuts import render, redirect, get_object_or_404
from .models import Clientes, Producto, Venta
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, ProductoForm
from django.http import HttpResponse
from django.db.models import Prefetch

from reportlab.pdfgen import canvas
from io import BytesIO

# Create your views here.

@login_required
def ventas_view(request):
    productos = Producto.objects.all()
    context = {
        'productos': productos,
    }
    return render(request, 'ventas.html', context)

@login_required
def clientes_view(request):
    clientes = Clientes.objects.all()
    context = {
        'clientes': clientes,
    }
    return render(request, 'clientes.html', context)

@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Clientes')  # Redirige a la lista de clientes
    else:
        form = ClienteForm()
    return render(request, 'clientes/agregar_cliente.html', {'form': form})

# Editar cliente
@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Clientes, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('Clientes')  # Redirige a la lista de clientes
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

# Eliminar cliente
@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Clientes, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('Clientes')  # Redirige a la lista de clientes
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})


@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/agregar_producto.html', {'form': form})

# Editar cliente
@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('Productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

# Eliminar cliente
@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('Productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})


@login_required
def generar_pdf(request):
    # Obtén los datos de la base de datos
    ventas = Producto.objects.all()

    # Crea un objeto BytesIO para almacenar el PDF
    buffer = BytesIO()

    # Crea el objeto PDF
    pdf = canvas.Canvas(buffer)

    # Agrega contenido al PDF
    pdf.drawString(100, 800, "Reporte de Productos")
    pdf.drawString(100, 780, "=" * 50)

    y = 750  # Posición vertical inicial
    for venta in ventas:
        pdf.drawString(100, y, f"ID Codigo: {venta.codigo}")
        pdf.drawString(100, y - 20, f"Producto: {venta.nombre}")
        pdf.drawString(100, y - 40, f"Descripcion: {venta.descripcion}")
        pdf.drawString(100, y - 60, f"Precio: {venta.precio}")
        pdf.drawString(100, y - 80, f"Cantidad: ${venta.cantidad}")
        pdf.drawString(100, y - 100, "=" * 50)
        y -= 120  # Ajusta la posición vertical para la siguiente venta

    # Finaliza el PDF
    pdf.showPage()
    pdf.save()

    # Obtén el valor del buffer y crea la respuesta HTTP
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
    return response


#carrito



# Función para agregar productos al carrito
def agregar_al_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)
    carrito = request.session.get('carrito', {})

    if str(id) not in carrito:
        carrito[str(id)] = {'nombre': producto.nombre, 'precio': float(producto.precio), 'cantidad': 1, 'stock': float(producto.cantidad)}
    else:
        if carrito[str(id)]['cantidad'] < producto.cantidad:  # Verificar el stock
            carrito[str(id)]['cantidad'] += 1

    request.session['carrito'] = carrito
    return redirect('Productos')

# Función para mostrar el carrito y calcular el total
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    clientes = Clientes.objects.all()
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total, 'clientes': clientes})

# Función para actualizar la cantidad en el carrito
def actualizar_carrito(request, id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})

        if str(id) in carrito:
            producto = get_object_or_404(Producto, id=id)
            if cantidad <= producto.cantidad:  # Verificar el stock
                carrito[str(id)]['cantidad'] = cantidad
                request.session['carrito'] = carrito

    return redirect('ver_carrito')

# Función para eliminar un producto del carrito
def eliminar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})

    if str(id) in carrito:
        del carrito[str(id)]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')

# Función para vaciar el carrito
def vaciar_carrito(request):
    request.session['carrito'] = {}
    return redirect('ver_carrito')




# views.py
@login_required
def realizar_compra(request):
    carrito = request.session.get('carrito', {})
    cliente_id = request.POST.get('cliente_id')  # Asume que seleccionas un cliente en el formulario

    if not carrito:
        return redirect('ver_carrito')

    cliente = get_object_or_404(Clientes, id=cliente_id)

    for id, item in carrito.items():
        producto = get_object_or_404(Producto, id=id)
        cantidad = item['cantidad']
        precio_unitario = item['precio']
        total = cantidad * precio_unitario

        # Crear la venta
        Venta.objects.create(
            cliente=cliente,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            total=total
        )

        # Actualizar el stock del producto
        producto.cantidad -= cantidad
        producto.save()

    # Vaciar el carrito
    request.session['carrito'] = {}
    return redirect('ver_carrito')  # Redirigir de vuelta al carrito

# generar reporte

@login_required
def generar_pdf_ventas(request):
    # Obtener todas las ventas agrupadas por cliente
    clientes_con_ventas = Clientes.objects.prefetch_related(
        Prefetch('venta_set', queryset=Venta.objects.select_related('producto').order_by('fecha_venta'))
    ).order_by('nombre')  # Ordenar clientes por nombre

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Configuración inicial
    pdf.setFont("Helvetica", 12)
    y = 750  # Posición vertical inicial
    page_number = 1

    # Título del reporte
    pdf.drawString(100, 800, f"Reporte de Ventas - Página {page_number}")
    pdf.drawString(100, 780, "=" * 50)

    for cliente in clientes_con_ventas:
        ventas_del_cliente = cliente.venta_set.all()

        if not ventas_del_cliente:
            continue

        pdf.drawString(100, y, f"Cliente: {cliente.nombre}")
        y -= 20

        total_compra = 0
        fecha_actual = None

        for venta in ventas_del_cliente:
            if y < 100:
                pdf.showPage()
                page_number += 1
                y = 750
                pdf.drawString(100, 800, f"Reporte de Ventas - Página {page_number}")
                pdf.drawString(100, 780, "=" * 50)
                pdf.drawString(100, y, f"Cliente: {cliente.nombre}")
                y -= 20

            # Si cambia la fecha, mostrar el total de la compra anterior
            if fecha_actual and fecha_actual != venta.fecha_venta.date():
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(120, y, f"Total Compra: {total_compra}")
                pdf.setFont("Helvetica", 12)
                y -= 20
                total_compra = 0  # Reiniciar el total para la nueva compra

            fecha_actual = venta.fecha_venta.date()  # Actualizar la fecha actual

            # Escribir detalles del producto
            pdf.drawString(120, y, f"Producto: {venta.producto.nombre}")
            pdf.drawString(120, y - 20, f"Cantidad: {venta.cantidad}")
            pdf.drawString(120, y - 40, f"Precio Unitario: {venta.precio_unitario}")
            pdf.drawString(120, y - 60, f"Total: {venta.total}")
            pdf.drawString(120, y - 80, f"Fecha: {venta.fecha_venta}")
            y -= 100

            total_compra += venta.total  # Acumular total de la compra actual

        # Imprimir el total de la última compra del cliente
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(120, y, f"Total Compra: {total_compra}")
        pdf.setFont("Helvetica", 12)
        y -= 20

        pdf.drawString(100, y, "=" * 50)
        y -= 20

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    # Devolver el PDF como respuesta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
    return response


