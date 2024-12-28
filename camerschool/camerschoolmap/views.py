from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'fontend/index.html')


def dashbord(request):
    return render(request, 'backend/dashbord.html')

def avis(request):
    return render(request, 'fontend/autres/avis.html')


def blog(request):
    return render(request, 'fontend/autres/blog.html')

def conf(request):
    return render(request, 'fontend/autres/conf.html')


def connexion(request):
    return render(request, 'fontend/autres/connexion.html')








# ======================= PARTIE LOGIQUE DU CONTACT US POUR L'ENVOIE D'UN MESSAGE============================
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect

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
    


