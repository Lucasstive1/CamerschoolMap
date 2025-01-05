from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User_View
import re
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.mail import send_mail
import os





# Create your views here.
def connexion(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        password = request.POST.get('password')
        
        print(f"Nom entré : {nom}")  # Debugging
        print(f"Mot de passe entré : {password}")  # Debugging
        print(os.getenv('EMAIL_HOST_USER')) # Debugging
        
        try:
            utilisateur = User_View.objects.get(nom=nom)
            print(f"Utilisateur trouvé : {utilisateur}")  # Debugging
            
            if check_password(password, utilisateur.password):
                request.session['utilisateur_id'] = utilisateur.id
                request.session['utilisateur_nom'] = utilisateur.nom
                request.session['utilisateur_email'] = utilisateur.email

                send_mail(
                    'Confirmation Mail',
                    'Vous vennez de vous connecter a votre profil CamerSchoolMap',
                    None,
                    [utilisateur.email],   # Destinataire
                    fail_silently=False,
                )
                
                
                return redirect("index")
            else:
                messages.error(request, "Nom ou Mot de passe incorrect")
        except User_View.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé")
            print("Utilisateur non trouvé dans la base de données")  # Debugging
    
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
           
         
        
        # Vérification de l'unicité de l'email
        if User_View.objects.filter(email=email).exists():  
            errors.append("Cet email est déjà utilisé.")
          
            
            
        if errors:
            return render(request, 'fontend/autres/inscription.html', {'errors': errors})

        
        user = User_View.objects.create(nom=nom, email=email, password=make_password(password), phone=phone)  
        user.save()
        messages.success(request, "Inscription reussir, connecter vous maintenant!")
        
        send_mail(
            'Confirmation Mail',
            "Vous vennez de faire une inscription sur CamerSchoolMap confirmer qu'il s'agit bien de vous ",
            None, # THIS IS THE MAIL OF THE SENDER, NONE IS PLACE HERE TO US THE CONFIGURATION EMAIL IN THE SETTING.PY
            [email],   # Destinataire
            fail_silently=False,
        )
        
          # Rediriger vers la page de connexion après l'inscription réussie
        return redirect('connexion')  #
            
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

