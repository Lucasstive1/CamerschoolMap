from django.db import models

# Create your models here.


# models pour lagestios des avis 
class Avis_views(models.Model):
    TYPE_CHOICES = [
        ('site','Site'),
        ('etablissement','Etablissement'),
    ]
    
    type_avis = models.CharField(max_length=20, choices=TYPE_CHOICES)
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    suject = models.CharField(max_length=200)
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} {self.suject}"
