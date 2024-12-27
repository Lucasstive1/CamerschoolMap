from django.urls import path
from . import views


urlpatterns = [
    path('index', views.index, name='index'),
    path('avis', views.avis, name='avis'),
    path('blog', views.blog, name='blog'),
    path('connexion', views.connexion, name='connexion'),
    path('contact', views.contact, name='contact'),
    path('detail', views.detail, name='detail'),
    path('conf', views.conf, name='conf'),
    path('mifi', views.mifi, name='mifi'),
    path('baf', views.baf, name='baf'),
]