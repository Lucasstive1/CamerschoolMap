from django.contrib import admin
from .models import Avis_views

# Register your models here.


class AdminAvis(admin.ModelAdmin):
    list_display = ('type_avis', 'nom', 'email', 'contenu', 'date')
    
    
admin.site.register(Avis_views  , AdminAvis)
