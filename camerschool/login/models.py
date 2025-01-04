from django.db import models
from django.utils import timezone


# Create your models here.
# models de creaction d'un utlisateur

class User_View(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    password = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nom 