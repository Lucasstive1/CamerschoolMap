from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Utilisateur', 'Utilisateur'),
        ('Chef d\'établissement', 'Chef d\'établissement'),
        ('Administrateur', 'Administrateur'),
    ]
    
    role = models.CharField(max_length=200, choices=ROLE_CHOICES, default='Utilisateur')
    phone = models.CharField(max_length=20, unique=True, null=True)
    
    def __str__(self):
        return f"{self.username} - {self.role}"
    
    def save(self, *args, **kwargs):
        """ Associe automatiquement l'utilisateur à un groupe selon son rôle """
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name=self.role)
        self.groups.add(group)

    
    
    def get_role_color(self):
        # Retourne une couleur en fonction du rôle
        if self.role == 'Administrateur':
            return 'success'  # Rouge
        elif self.role == 'Chef d\'établissement':
            return 'primary'  # Jaune
        else:
            return 'primary'  # Vert
    
    