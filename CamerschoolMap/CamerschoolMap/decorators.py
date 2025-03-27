from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def login_required_message(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('connexion')  # Remplacez 'connexion' par le nom de votre url de connexion
        return view_func(request, *args, **kwargs)
    return wrapper
