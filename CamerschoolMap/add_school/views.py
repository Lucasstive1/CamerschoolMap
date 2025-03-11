from django.contrib import messages
from .models import Etablissement, PhotoEtablissement
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect

def is_admin(user):
    return user.groups.filter(name='Administrateur').exists()

def is_chef(user):
    return user.groups.filter(name="Chef d'établissement").exists()

def ajouter_etablissement(request):
    if request.method == 'POST':
        erreurs = []

        # Récupération des données
        nom = request.POST.get('nom', '').strip()
        ville = request.POST.get('ville', '').strip()
        departement = request.POST.get('departement', '').strip()
        type_etablissement = request.POST.get('type', '').strip()
        categorie = request.POST.get('categories', '').strip()
        description = request.POST.get('description', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        contact = request.POST.get('contact', '').strip()
        email = request.POST.get('email', '').strip()

        # Vérification des champs obligatoires
        if not nom:
            erreurs.append("Le champ 'Nom de l'établissement' est requis.")
        if not ville:
            erreurs.append("Le champ 'Ville' est requis.")
        if not type_etablissement:
            erreurs.append("Le champ 'Type' est requis.")
        if not categorie:
            erreurs.append("Le champ 'Catégorie' est requis.")
        if not adresse:
            erreurs.append("Le champ 'Adresse' est requis.")

        # Vérification de l'email
        if email and '@' not in email:
            erreurs.append("Veuillez entrer une adresse email valide.")

        # Gestion des fichiers
        image_profil = request.FILES.get('image_profil', None)
        photos = request.FILES.getlist('photos')

        # S'il y a des erreurs, on affiche les messages
        if erreurs:
            for erreur in erreurs:
                messages.error(request, erreur)
            return redirect('school')

        # Création de l'établissement
        etablissement = Etablissement(
            nom=nom,
            ville=ville,
            departement=departement,
            type=type_etablissement,
            categorie=categorie,
            description=description,
            adresse=adresse,
            contact=contact,
            email=email
        )

        # Sauvegarde de l'image de profil
        if image_profil:
            etablissement.image_profil = image_profil

        # Sauvegarde en base de données
        etablissement.save()

        # Sauvegarde des photos supplémentaires
        for photo in photos:
            PhotoEtablissement.objects.create(etablissement=etablissement, image=photo)

        # messages.success(request, "Établissement ajouté avec succès !")
        return redirect('succes_page')

    return render(request, 'backend/autres/school.html')




@user_passes_test(is_admin, login_url='echecs')
def supprimer_etablissement(request, etablissement_id):
    if request.method == "POST":
        try:
            etablissement = Etablissement.objects.get(id=etablissement_id)
            etablissement.delete()
            messages.success(request, "Établissement supprimé avec succès !")
            return JsonResponse({"success": True})
        except Etablissement.DoesNotExist:
            return JsonResponse({"success": False, "error": "Établissement introuvable."})
    return JsonResponse({"success": False, "error": "Requête invalide."})

@user_passes_test(is_admin, login_url='echecs')
def modifier_etablissement(request, etablissement_id):
    if request.method == "POST":
        try:
            etablissement = Etablissement.objects.get(id=etablissement_id)

            # Lire les données envoyées en JSON
            data = json.loads(request.body)

            # Récupération des valeurs
            nom = data.get('nom', '').strip()
            ville = data.get('ville', '').strip()
            type_etablissement = data.get('type', '').strip()
            categorie = data.get('categorie', '').strip()
            adresse = data.get('adresse', '').strip()
            contact = data.get('contact', '').strip()
            email = data.get('email', '').strip()

            # Vérification des champs obligatoires
            if not nom or not ville or not type_etablissement or not categorie or not adresse:
                return JsonResponse({"success": False, "error": "Tous les champs obligatoires doivent être remplis."})

            # Mise à jour des informations
            etablissement.nom = nom
            etablissement.ville = ville
            etablissement.type = type_etablissement
            etablissement.categorie = categorie
            etablissement.adresse = adresse
            etablissement.contact = contact
            etablissement.email = email
            etablissement.save()

            return JsonResponse({"success": True})

        except Etablissement.DoesNotExist:
            return JsonResponse({"success": False, "error": "Établissement introuvable."})

    return JsonResponse({"success": False, "error": "Requête invalide."})





def succes_page(request):
    return render(request, 'backend/autres/succes.html')

def echecs(request):
    return render(request, 'backend/autres/echecs.html')

def erreur_403(request):
    return render(request, 'backend/autres/error-404.html', status=403)


def detail(request):
    etablissements = Etablissement.objects.all()

    nom = request.GET.get('nom', '').strip()
    ville = request.GET.get('ville', '').strip()
    departement = request.GET.get('departement', '').strip()
    type_etablissement = request.GET.get('type', '').strip()
    categorie = request.GET.get('categorie', '').strip()

    if nom:
        etablissements = etablissements.filter(nom__icontains=nom)
    if ville:
        etablissements = etablissements.filter(ville__icontains=ville)
    if departement:
        etablissements = etablissements.filter(departement__icontains=departement)
    if type_etablissement:
        etablissements = etablissements.filter(type__icontains=type_etablissement)
    if categorie:
        etablissements = etablissements.filter(categorie__icontains=categorie)

    # Pagination : 10 établissements par page
    paginator = Paginator(etablissements, 6)
    page_number = request.GET.get('page')
    etablissements = paginator.get_page(page_number)

    return render(request, 'backend/autres/detail.html', {'etablissements': etablissements})


def detail_etablissement(request, etablissement_id):
    etablissement = get_object_or_404(Etablissement, id=etablissement_id)
    return render(request, 'fontend/autres/detail.html', {'etablissement': etablissement})


@login_required(login_url='connexion')
def historique_ecole(request):
    etablissements_list = Etablissement.objects.all()

    # Définir le nombre d'éléments par page
    paginator = Paginator(etablissements_list, 20)  # 6 établissements par page
    page_number = request.GET.get('page')
    etablissements = paginator.get_page(page_number)

    return render(request, 'backend/autres/historique_ecole.html', {'etablissements': etablissements})
