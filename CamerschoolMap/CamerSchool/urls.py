from django.urls import path
from CamerSchool import views

urlpatterns  = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('contact', views.contact, name='contact'),
    path('avis', views.avis, name='avis'),
    path('supprimer-avis/<int:avis_id>/', views.supprimer_avis, name='supprimer_avis'),
]