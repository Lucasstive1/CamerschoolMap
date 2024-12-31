from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('dashbord', views.dashbord, name='dashbord'),
    path('avis', views.avis, name='avis'),
    path('blog', views.blog, name='blog'),
    path('connexion', views.connexion, name='connexion'),
    path('inscription', views.inscription, name='inscription'),
    path('contact', views.contact, name='contact'),
    path('detail', views.detail, name='detail'),
    path('conf', views.conf, name='conf'),
    path('mifi', views.mifi, name='mifi'),
    path('baf', views.baf, name='baf'),
    path('school', views.school, name='school'),
    path('register', views.register, name='register'),
    path('error', views.error, name='error-404'),
    path('setting', views.setting, name='setting'),
    path('confirmation', views.confirmation, name='confirmation'),
    
]