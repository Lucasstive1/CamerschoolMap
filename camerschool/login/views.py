from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import User_View
import re
from django.core.paginator import Paginator



# Create your views here.
def connexion(request):
    return render(request, 'fontend/autres/connexion.html')


def inscription(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        errors = []
        
        # verification du format de l'email
        # validation de l'email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append( "L'adresse email n'est pas valide.")
        
        
         # Vérification du mot de passe
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)', password):
            errors.append("Le mot de passe doit contenir au moins une majuscule et un chiffre.")
            
        # verification du numero de telephone 
        if not re.match(r'^\+237\s\d{3}\s\d{3}\s\d{3}$', phone):
           errors.append("Numéro de téléphone invalide. Format attendu : +237 XXX XXX XXX")
           
        # Vérification de l'unicité du username
        if User_View.objects.filter(nom=nom).exists():  # Remplace "User" par "CustomUser"
            errors.append("Ce nom d'utilisateur existe déjà.")
         
        
#        # Vérification de l'unicité de l'email
        if User_View.objects.filter(email=email).exists():  # Remplace "User" par "CustomUser"
            errors.append("Cet email est déjà utilisé.")
          
            
            
        if errors:
            return render(request, 'fontend/autres/inscription.html', {'errors': errors})

        
        user = User_View.objects.create(nom=nom, email=email, password=password, phone=phone)  # Remplace "User" par "CustomUser"
        user.save()
        messages.success(request, "Inscription reussir, connecter vous maintenant!")
        
          # Rediriger vers la page de connexion après l'inscription réussie
        return redirect('connexion')  #
            
    return render(request, 'fontend/autres/inscription.html')



def historique(request):
    
    users = User_View.objects.all()
    
    # Pagination
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'backend/autres/historique.html', {'users': users})
