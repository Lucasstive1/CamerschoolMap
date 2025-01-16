from django.urls import path
from . import views


urlpatterns = [
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('historique/', views.historique, name='historique'),
    path('deconnexion/', views.confirmation_deconnexion, name='confirmation_deconnexion'),
    path('modifieruser/<int:id>/', views.modifieruser, name='modifieruser'),
    path('suppression_user/<int:id>/', views.suppression_user, name='suppression_user'),
    path('register', views.register, name='register'),
    path('dashbord', views.dashbord, name='dashbord'),

    
]