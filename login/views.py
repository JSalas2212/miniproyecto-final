from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

# Create your views here.

@login_required
def home(request):
    return render(request, 'login/home.html')

def user_login(request):
    # Si el usuario ya está autenticado, redirige al home
    if request.user.is_authenticated:
        return redirect('home')  # Redirige a la página de inicio

    # Si el usuario no está autenticado, muestra el formulario de login
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige al home después del login
    else:
        form = AuthenticationForm()

    return render(request, 'login/login.html', {'form': form})

def user_logout(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige al login después de cerrar sesión