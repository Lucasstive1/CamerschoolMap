from django.contrib import admin
from .models import User_View

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "email", "password", "phone")
    list_filter = ("id", "nom", "email")
    
admin.site.register(User_View  , UserAdmin)
