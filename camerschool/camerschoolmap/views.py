from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import Avis_views
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'fontend/index.html')


def dashbord(request):
    return render(request, 'backend/dashbord.html')




#====================== fonction pour la gestion des avis =======================
def avis(request):
    # Récupération des avis
    avis_list = Avis_views.objects.all().order_by('-date')

    # Gestion de la barre de recherche
    avis_search = request.GET.get('avis-search')
    if avis_search and avis_search.strip():  # Vérifie si la recherche n'est pas vide
        avis_list = avis_list.filter(suject__icontains=avis_search)

    # Pagination
    paginator = Paginator(avis_list, 3)
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








def blog(request):
    return render(request, 'fontend/autres/blog.html')

def conf(request):
    return render(request, 'fontend/autres/conf.html')



# ======================== partie connexion pour les utlisateur ===============================
def connexion(request):
    if request.method == 'POST':
        name = request.POST.get('nom', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        phone_number = request.POST.get('phone', None)
        print("=="*5, "nouvelle connexion pour", name, "ayant pour adresse:", email, "et pour numero :", phone_number, "=="*5)
    return render(request, 'fontend/autres/connexion.html')








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
            subject_mail,
            body,
            email,
            ['stivelucas037@gmail.com'],
            fail_silently=False,
            html_message=body  # Utilisation du format HTML
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
    return render(request, 'fontend/autres/detail.')

def mifi(request):
    return render(request, 'fontend/departement/mifi.html')

def baf(request):
    return render(request, 'fontend/villes/baf.html')

def register(request):
    return render(request, 'backend/autres/register.html')

def school(request):
    return render(request, 'backend/autres/school.html')

def historique(request):
    return render(request, 'backend/autres/historique.html')

def error(request):
    return render(request, 'backend/autres/error-404.html')

def setting(request):
    return render(request, 'backend/autres/setting.html')
    


