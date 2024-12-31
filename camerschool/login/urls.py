from django.urls import path
from . import views


urlpatterns = [
    path('/connexion', views.connexion, name='connexion'),
    path('/inscription', views.inscription, name='inscription'),
    path('/historique', views.historique, name='historique'),
    
]