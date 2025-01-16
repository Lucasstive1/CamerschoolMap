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








# fonctions de creation d'un utlisateur par l'admin

from django.contrib import messages  # Assurez-vous que cette importation est présente

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')
        password = request.POST.get('password')
        
        errors = []
        
        # Validation des champs
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append("Format d'email invalide.")
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password):
            errors.append("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")
        if not re.match(r'^\+237\d{9}$', phone_number):
            errors.append("Le numéro de téléphone doit être au format +237XXXXXXXXX.")
        if CustomUser.objects.filter(email=email).exists():
            errors.append("L'email existe déjà.")
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            errors.append("Le numéro de téléphone que vous avez entré existe déjà. Veuillez réessayer.")
        
        # Gestion des erreurs
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'backend/autres/register.html')
        
        # Création de l'utilisateur
        user = CustomUser.objects.create(
            username=username,
            email=email,
            role=role,
            phone_number=phone_number,
            password=make_password(password),
        )
        
        # Envoi de l'email
        send_mail(
            subject='Inscription réussie sur le site',
            message=(
                f"Bonjour {username},\n\n"
                f"Votre compte a été créé avec succès !\n\n"
                f"Identifiants :\nNom d'utilisateur : {username}\nMot de passe : {password}\n\n"
                f"Merci de nous avoir rejoints !"
            ),
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )
        
        messages.success(request, "Utilisateur ajouté avec succès !")
        return redirect('register')  # Redirection pour recharger la page et vider le formulaire
    
    return render(request, 'backend/autres/register.html')




def dashbord(request):
    utilisateurs = CustomUser.objects.all().order_by('-id')  # Tri par ID décroissant
    paginator = Paginator(utilisateurs, 10)  # 10 utilisateurs par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'backend/dashbord.html', {'page_obj': page_obj})



# def historique_utilisateurs(request):
#     utilisateurs = CustomUser.objects.all().order_by('-id')  # Tri par ID décroissant
#     paginator = Paginator(utilisateurs, 10)  # 10 utilisateurs par page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     return render(request, 'backend/autres/historique.html', {'page_obj': page_obj})
