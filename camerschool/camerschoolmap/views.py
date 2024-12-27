from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'fontend/index.html')


def avis(request):
    return render(request, 'fontend/autres/avis.html')


def blog(request):
    return render(request, 'fontend/autres/blog.html')

def conf(request):
    return render(request, 'fontend/autres/conf.html')


def connexion(request):
    return render(request, 'fontend/autres/connexion.html')


def contact(request):
    return render(request, 'fontend/autres/contact.html')

def detail(request):
    return render(request, 'fontend/autres/detail.')

def mifi(request):
    return render(request, 'fontend/departement/mifi.html')

def baf(request):
    return render(request, 'fontend/villes/baf.html')


