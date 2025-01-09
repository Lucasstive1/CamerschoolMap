from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, JsonResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import Avis_views
from django.contrib import messages



# Create your views here
def index(request):
     # Récupération des avis
    avis_list = Avis_views.objects.all().order_by('-date')
    if 'utilisateur_id' not in request.session:
        return redirect('connexion')  # Rediriger vers la page de connexion si non connecté

    # Informations de l'utilisateur connecté
    utilisateur_nom = request.session['utilisateur_nom']
    return render(request, 'fontend/index.html', {'nom': utilisateur_nom})








#====================== fonction pour la gestion des avis =======================
def avis(request):
    # Récupération des avis
    avis_list = Avis.objects.all().order_by('-date')  # Obtenez les avis récents
    paginator = Paginator(avis_list, 5)  # Paginer par 5 avis

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Gestion de la barre de recherche
    avis_search = request.GET.get('avis-search')
    if avis_search and avis_search.strip():  # Vérifie si la recherche n'est pas vide
        avis_list = avis_list.filter(suject__icontains=avis_search)

    # Pagination
    paginator = Paginator(avis_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        # Récupération des données du formulaire
        type_avis = request.POST.get('typeAvis')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        suject = request.POST.get('suject')
        contenu = request.POST.get('contenu')

        try:
            # Création d'un nouvel avis
            Avis_views.objects.create(
                type_avis=type_avis,
                nom=nom,
                email=email,
                suject=suject,
                contenu=contenu
            )
            messages.success(request, "Avis enregistré avec succès.")  # Message de succès
        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement de l'avis : {str(e)}")  # Message d'erreur

    return render(request, 'fontend/autres/avis.html', {'page_obj': page_obj})




    
def supprimer_avis(request, avis_id):
    if request.method == "POST":
        try:
            avis = Avis_views.objects.get(id=avis_id)
            avis.delete()
            return JsonResponse({'success': True, 'message': 'Avis supprimé avec succès!'})
        except Avis_views.DoesNotExist:
            return JsonResponse({'success': False, 'message': "L'avis n'existe pas."})
    return JsonResponse({'success': False, 'message': 'Requête invalide.'})








def blog(request):
    return render(request, 'fontend/autres/blog.html')

def conf(request):
    return render(request, 'fontend/autres/conf.html')




def inscription(request):
    return render(request, 'fontend/autres/inscription.html')





# ======================= PARTIE LOGIQUE DU CONTACT US POUR L'ENVOIE D'UN MESSAGE============================  
def contact(request):
    if request.method == 'POST':
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        
        # Sujet de l'email
        subject_mail = f"Message de {nom} {prenom}"
        
        # Corps de l'email avec format HTML pour un rendu plus professionnel
        body = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333;
                }}
                .email-container {{
                    background-color: #f4f4f4;
                    padding: 20px;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                }}
                h2 {{
                    color: #333;
                    font-size: 18px;
                    font-weight: bold;
                }}
                p {{
                    font-size: 16px;
                    line-height: 1.5;
                }}
                .highlight {{
                    font-weight: bold;
                    color: #007BFF;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <h2>Message reçu de {nom} {prenom}</h2>
                <p><span class="highlight">Nom:</span> {nom}</p>
                <p><span class="highlight">Prénom:</span> {prenom}</p>
                <p><span class="highlight">Email:</span> {email}</p>
                <p><span class="highlight">Numéro de téléphone:</span> {phone}</p>
                <p><span class="highlight">Sujet:</span> {subject}</p>
                <p><span class="highlight">Message:</span> <br>{message}</p>
            </div>
        </body>
        </html>
        """

        # Envoi de l'email
        send_mail(
            'Contact',
            'Merci de nous avoir contacter nous traitons votre demande et nous vous reviendrons bientot',
            None,
            [email],   # Destinataire
            fail_silently=False,
        )

        # Redirection vers la page de confirmation
        return redirect(reverse('confirmation') + f'?nom={nom}&email={email}')

    return render(request, 'fontend/autres/contact.html')



def confirmation(request : HttpRequest):
    nom = request.GET.get('nom')
    email = request.GET.get('email')
    
    context = { 'nom': nom, 'email': email}
                   
    return render(request, 'fontend/autres/confirmation.html', context)


def detail(request):
    return render(request, 'fontend/autres/detail.html')

def mifi(request):
    return render(request, 'fontend/departement/mifi.html')

def baf(request):
    return render(request, 'fontend/villes/baf.html')



def school(request):
    return render(request, 'backend/autres/school.html')


def error(request):
    return render(request, 'backend/autres/error-404.html')

def setting(request):
    return render(request, 'backend/autres/setting.html')
    


