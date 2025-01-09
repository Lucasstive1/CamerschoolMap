from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User_View
from .models import CustomUser 
import re
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.mail import send_mail
import os
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group





# Create your views here.
def connexion(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        password = request.POST.get('password')

        try:
            utilisateur = User_View.objects.get(nom=nom)

            if check_password(password, utilisateur.password):
                request.session['utilisateur_id'] = utilisateur.id
                request.session['utilisateur_nom'] = utilisateur.nom
                request.session['utilisateur_email'] = utilisateur.email

                # Envoyer un email
                send_mail(
                    'Confirmation Mail',
                    'Vous venez de vous connecter à votre profil CamerSchoolMap',
                    None,
                    [utilisateur.email],
                    fail_silently=False,
                )

                messages.success(request, "Connexion réussie ! Bienvenue, {}.".format(utilisateur.nom))
                return redirect("index")
            else:
                messages.error(request, "Nom ou mot de passe incorrect")
        except User_View.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé dans la base de données")

    return render(request, 'fontend/autres/connexion.html')



def inscription(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        errors = []
        
        # Validation email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append("L'adresse email n'est pas valide.")
        
        # Vérification du mot de passe
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)', password):
            errors.append("Le mot de passe doit contenir au moins une majuscule et un chiffre.")
            
        # Vérification du téléphone
        if not re.match(r'^\+237\s\d{3}\s\d{3}\s\d{3}$', phone):
            errors.append("Numéro de téléphone invalide. Format attendu : +237 XXX XXX XXX")
        
        # Vérification de l'unicité de l'email
        if User_View.objects.filter(email=email).exists():  
            errors.append("Cet email est déjà utilisé.")
        
        # Vérification de l'unicité du nom
        if User_View.objects.filter(nom=nom).exists():
            errors.append("Un utilisateur avec ce nom existe déjà.")
        
        if errors:
            return render(request, 'fontend/autres/inscription.html', {'errors': errors})
        
        # Création de l'utilisateur
        user = User_View.objects.create(
            nom=nom, email=email, 
            password=make_password(password), phone=phone
        )  
        user.save()
        messages.success(request, "Inscription réussie, connectez-vous maintenant!")
        
        # Envoi d'email
        send_mail(
            'Confirmation Mail',
            "Vous venez de vous inscrire sur CamerSchoolMap, confirmez qu'il s'agit bien de vous.",
            None,  # Utilise la configuration EMAIL dans settings.py
            [email], 
            fail_silently=False,
        )
        
        return redirect('connexion')
    
    return render(request, 'fontend/autres/inscription.html')

def historique(request):
    
    users = User_View.objects.all().order_by('-id')

    
    # Pagination
    paginator = Paginator(users, 50)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'backend/autres/historique.html', {'users': users})



# fonction de la deconnection
def deconnexion(request):
    if 'utilisateur_id' in request.session:
        del request.session['utilisateur_id']
        del request.session['utilisateur_nom']
        del request.session['utilisateur_email']    

    logout(request)
    return redirect('connexion')


def confirmation_deconnexion(request):
    if request.method == 'POST':
        # Si l'utilisateur confirme, déconnectez-le
        if 'utilisateur_id' in request.session:
            del request.session['utilisateur_id']
            del request.session['utilisateur_nom']
            del request.session['utilisateur_email']
        logout(request)
        return redirect('connexion')  # Redirige vers la page de connexion

    # Affiche la page de confirmation
    return render(request, 'fontend/autres/confirmation_deconnexion.html', {
        'utilisateur_nom': request.session.get('utilisateur_nom', 'Utilisateur')
    })

    
    
    
    
    
# fonction de modification d'un user
def modifieruser(request, id):
    try:
        utilisateur = User_View.objects.get(id = id)
        if request.method == 'POST':
            nom = request.POST.get('nom')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            
            errors = []
            
            # Validation des champs
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                errors.append("L'adresse email n'est pas valide.")

            if not re.match(r'^\+237\s\d{3}\s\d{3}\s\d{3}$', phone):
                errors.append("Numéro de téléphone invalide. Format attendu : +237 XXX XXX XXX")

            if errors:
                return render(request, 'backend/autres/modifieruser.html', {'id': id, 'errors': errors, 'utilisateur': utilisateur})
            
            
            # Mise à jour des informations
            utilisateur.nom = nom
            utilisateur.email = email
            utilisateur.phone = phone
            utilisateur.save()
            
            
            messages.success(request, f"Les informations de l'utilisateur {id} ont été mises à jour avec succès.")
            return redirect('historique')

        return render(request, 'backend/autres/modifieruser.html', {'id': id, 'utilisateur': utilisateur})
    except User_View.DoesNotExist:
        messages.error(request, "L'utilisateur n'existe pas.")
        return redirect('historique')



def suppression_user(request, id):
    if request.method == 'POST':
        try:
            utilisateur = User_View.objects.get(id=id)
            utilisateur.delete()
            return JsonResponse({'success': True, 'message': 'Utilisateur supprimé avec succès.'})
        except User_View.DoesNotExist:
            return JsonResponse({'success': False, 'message': "L'utilisateur n'existe pas."})
    return JsonResponse({'success': False, 'message': 'Requête invalide.'})



User = get_user_model()


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        # phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        
        
        # verification de l'existence de l'utlisateur
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur existe déjà.')
            return redirect('dashbord')
        
        
         # Créer l'utilisateur
        user = User.objects.create_user(username=username, email=email, password=password)
         
          # Ajouter l'utilisateur au groupe en fonction du rôle
        if role == 'Chef d\'etablissement':
            group = Group.objects.get(name='Head of Institution')
            user.is_head_of_institution = True
        elif role == 'Administrateur':
            group = Group.objects.get(name='Admin')
            user.is_admin = True
        else:
            group = Group.objects.get(name='User')

        user.groups.add(group)
        user.save()
                
        messages.success(request, 'Utilisateur ajouté avec succès!')
        return redirect('register')
    return render(request, 'backend/autres/register.html')


def dashbord(request):
    return render(request, 'backend/dashbord.html')


