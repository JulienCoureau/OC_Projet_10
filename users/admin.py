from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Affiche le modèle User custom dans l'admin Django avec les champs RGPD."""
    list_display = (
        "id", "username", "email", "birth_date",
        "can_be_contacted", "can_data_be_shared", "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "can_be_contacted")
    search_fields = ("username", "email")

    fieldsets = UserAdmin.fieldsets + (
        ("Informations RGPD", {
            "fields": ("birth_date", "can_be_contacted", "can_data_be_shared")
        }),
    )