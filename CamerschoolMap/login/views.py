from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import re
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt


def is_admin(user):
    return user.groups.filter(name='Administrateur').exists()

def is_chef(user):
    return user.groups.filter(name="Chef d'établissement").exists()


def erreur_403(request):
    return render(request, 'backend/autres/error-404.html', status=403)



User = get_user_model()
# Fonction de D'INSCRIPTION
def inscription(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        errors = []
        
        # Vérification des formats
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password):
            errors.append("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")
        if not re.match(r'^\+237\d{9}$', phone):
            errors.append("Le numéro de téléphone doit être au format +237XXXXXXXXX.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append("Format d'email invalide.")
        
        # Vérification unicité de l'email
        if User.objects.filter(email=email).exists():
            errors.append("L'email existe déjà.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'fontend/autres/inscription.html')

        # Création de l'utilisateur (NE PAS HACHER LE MOT DE PASSE MANUELLEMENT)
        user = User.objects.create_user(username=nom, email=email, password=password)
        messages.success(request, "Inscription reussite! Vous pouvez maintenant vous connecter a votre compte😊")
        return redirect('connexion')
    
    return render(request, 'fontend/autres/inscription.html')














@csrf_exempt
# Fonction de connexion
def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Vérification des champs vides
        if not email or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect('connexion')

        # Récupération de l'utilisateur avec cet email
        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                messages.success(request, f"Conexion reussir avec success.\n Bienvenue, {auth_user.username} !")
                return redirect('detail')

        messages.error(request, "Email ou mot de passe incorrect.Merci de ressayer ulterrieurement")
    
    return render(request, 'fontend/autres/connexion.html')

















# FOCTION DE DECONNEXION 
@login_required(login_url='connexion')
def deconnexion(request):
    if request.method == "POST":
        logout(request)
        request.session.flush()
        print("Déconnexion effectuée et session supprimée.")
        return JsonResponse({"message": "Vous avez été déconnecté avec succès."})
    
    return JsonResponse({"error": "Méthode non autorisée."}, status=400)









@login_required(login_url='connexion')
def historique(request):
    users = User.objects.all().order_by('-id')
    # Pagination
    paginator = Paginator(users, 50)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'backend/autres/historique.html', {'users': users})













# FONCTION POUR SUPPRIMER UN UTLISATEUR 
@login_required(login_url='connexion')
def supprimer_user(request):
    if request.method == 'POST':
        try:
            # Récupérer les données JSON de la requête
            data = json.loads(request.body)
            user_id = data.get('user_id')  # Récupérer l'ID de l'utilisateur

            # Vérifier si l'utilisateur existe
            utilisateur = User.objects.get(id=user_id)
            utilisateur.delete()
            return JsonResponse({'status': 'success', 'message': 'Utilisateur supprimé avec succès.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "L'utilisateur n'existe pas."})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Requête invalide.'})







# FONCTION POUR MODIFIER UN UTILISATEUR
@login_required(login_url='connexion')
def modifier_user(request, user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        messages.error(request, "L'utilisateur demandé n'existe pas.")
        return redirect('users_list')  # Rediriger vers la liste des utilisateurs si l'utilisateur n'existe pas.

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        errors = []
        
        # Vérification des formats
        if not re.match(r'^[a-zA-Z0-9_]+$', nom):  # Vérification pour le nom d'utilisateur
            errors.append("Le nom ne doit contenir que des lettres et des chiffres.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):  # Vérification pour l'email
            errors.append("Format d'email invalide.")
        
        if password:
            if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password):  # Vérification du mot de passe
                errors.append("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")
        
        # Vérification unicité de l'email (si l'email a changé)
        if email != user.email and User.objects.filter(email=email).exists():
            errors.append("L'email existe déjà.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'backend/autres/modifieruser.html', {'user': user})

        # Mise à jour des données de l'utilisateur
        user.username = nom
        user.email = email
        if password:
            user.set_password(password)  # Ne pas oublier de hacher le mot de passe
        user.save()
        
        messages.success(request, "Utilisateur modifié avec succès!")
        return redirect('historique')  # Redirige vers la liste des utilisateurs

    return render(request, 'backend/autres/modifieruser.html', {'user': user})

    
    
# FONCTION QUI PERMET A L'AMINISTRATEUR D'AJOUTER DES NEMBRES
@login_required(login_url='connexion')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', 'Utilisateur') 
        
        errors = []

        # Vérifier si les valeurs ne sont pas vides
        if not username or not phone or not password or not email:
            errors.append("Tous les champs doivent être remplis.")

        # Vérifications de la validité des champs (uniquement si les valeurs ne sont pas None)
        if username and not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append("Le nom d'utilisateur ne doit contenir que des lettres, chiffres et underscore.")
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append("Format d'email invalide.")
        if phone and not re.match(r'^\+237\d{9}$', phone):
            errors.append("Le numéro de téléphone doit être au format +237XXXXXXXXX.")
        if password and not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password):
            errors.append("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")

        # Vérification unicité des données
        if CustomUser.objects.filter(email=email).exists():
            errors.append("L'email existe déjà.")
        if CustomUser.objects.filter(phone=phone).exists():
            errors.append("Le numéro de téléphone est déjà utilisé.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'backend/autres/register.html')

        # Création de l'utilisateur
        user = CustomUser.objects.create(
            username=username,
            email=email,
            role=role,
            phone=phone,
            password=make_password(password)
        )

        messages.success(request, "Utilisateur ajouté avec succès !")
        return redirect('historique')

    return render(request, 'backend/autres/register.html')

# FONCTION POUR AFFICHER LES UTILISATEURS ET GERER LA PAGINATION
@login_required(login_url='connexion')
@user_passes_test(is_admin, login_url='echecs')
def dashboard(request):
    users_list = CustomUser.objects.exclude(id=request.user.id)
    total_utilisateurs = CustomUser.objects.count()
    total_chefs = CustomUser.objects.filter(role='Chef d\'établissement').count()
    
    # Pagination : 10 établissements par page
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    etablissements = paginator.get_page(page_number)
    
    context = {
        'total_utilisateurs': total_utilisateurs,
        'total_chefs': total_chefs,
        'users_list': users_list,
        'etablissements': etablissements
    }
    
    return render(request, 'backend/dashbord.html', context)


@login_required(login_url='connexion')
def setting(request):
    user = request.user

    if request.method == 'POST':
        # Mise à jour des informations de l'utilisateur
        user.first_name = request.POST.get('fullName', user.first_name)
        user.phone = request.POST.get('phoneNumber', user.phone)
        user.email = request.POST.get('email', user.email)
        user.bio = request.POST.get('bio', user.bio)

        # Vérifier si un nouveau mot de passe est entré et mettre à jour
        password = request.POST.get('password')
        if password:
            user.set_password(password)

        # Sauvegarde de l'utilisateur
        user.save()
        messages.success(request, "Vos paramètres ont été mis à jour avec succès!")

        return redirect('settings')  # Rediriger vers la même page après mise à jour
    return render(request, 'backend/autres/settings.html', {'user': user})










def modifieruser(request):
    return render(request, 'backend/autres/modifieruser.html')





def conf(request):
    return render(request, 'fontend/autres/conf.html')








def error(request):
    return render(request, 'backend/autres/error-404.html')

def confirmation(request):
    return render(request, 'fontend/autres/confirmation.html')



def baf(request):
    return render(request, 'fontend/villes/baf.html')




@login_required(login_url='connexion')
def confirmation_deconnexion(request):
    return render(request, 'fontend/autres/confirmation_deconnexion.html')


