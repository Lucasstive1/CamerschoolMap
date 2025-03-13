from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Avis_views
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    
    if User is authenticate:
        return   messages.success(request, 'bienvenue sur camerschool')
  
    villes = [
        {"name": "Ouest", "image": "fontend/images/bafoussam-ville.jpg.webp"},
        {"name": "Adamawa", "image": "fontend/images/adamawa.jpg"},
        {"name": "Nord-Ouest", "image": "fontend/images/Bamenda.jpg"},
        {"name": "Centre", "image": "fontend/images/Yaounde.jpg"},
        {"name": "Littoral", "image": "fontend/images/douala.jpg"},
        {"name": "Sud-cameroun", "image": "fontend/images/ebolowa.jpg"},
        {"name": "Extrême-Nord", "image": "fontend/images/Maroua-Art.png"},
        {"name": "Nord-cameroun", "image": "fontend/images/GAROUA.jpg"},
        {"name": "sud-ouest", "image": "fontend/images/GAROUA.jpg"},
        {"name": "Est-cameroun", "image": "fontend/images/GAROUA.jpg"},
        
    ]
    

    # Pagination
    paginator = Paginator(villes, 2)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)


    # Passe les données de l'utilisateur au template
    return render(request, 'fontend/index.html', {  'page_obj': page_obj})


def blog(request):
    return render(request, 'fontend/autres/blog.html')


@login_required(login_url='connexion')
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
            [message], # Message
            fail_silently=False,
        )

        # Redirection vers la page de confirmation
        return redirect(reverse('confirmation') + f'?nom={nom}&email={email}')

    return render(request, 'fontend/autres/contact.html')


@login_required(login_url='connexion')
def avis(request):
    # Récupération et tri des avis par date décroissante
    avis_list = Avis_views.objects.all().order_by('-date')

    # Gestion de la barre de recherche (le champ input devra avoir name="avis-search")
    avis_search = request.GET.get('avis-search')
    if avis_search and avis_search.strip():
        avis_list = avis_list.filter(nom__icontains=avis_search) | avis_list.filter(contenu__icontains=avis_search)

    # Pagination (30 avis par page)
    paginator = Paginator(avis_list, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        # Récupération des données du formulaire
        type_avis = request.POST.get('typeAvis')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        contenu = request.POST.get('contenu')

        try:
            # Création d'un nouvel avis
            Avis_views.objects.create(
                type_avis=type_avis,
                rating=rating,
                nom=nom,
                email=email,
                contenu=contenu
            )
            messages.success(request, "Avis enregistré avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement de l'avis : {str(e)}")

        return redirect('avis')  # redirige pour éviter le re-post du formulaire

    return render(request, 'fontend/autres/avis.html', {'page_obj': page_obj})




# ============== fonction de suppression d'un avis ==========
def supprimer_avis(request, avis_id):
    if request.method == "POST":
        try:
            logger.info(f"Tentative de suppression de l'avis avec l'ID : {avis_id}")
            avis = Avis_views.objects.get(id=avis_id)
            avis.delete()
            return JsonResponse({'success': True, 'message': 'Avis supprimé avec succès!'})
        except Avis_views.DoesNotExist:
            logger.error(f"Avis avec l'ID {avis_id} non trouvé.")
            return JsonResponse({'success': False, 'message': "L'avis n'existe pas."})
    return JsonResponse({'success': False, 'message': 'Requête invalide.'})