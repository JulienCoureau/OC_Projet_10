from rest_framework import serializers
from .models import User
from datetime import date

class UserSerializer (serializers.ModelSerializer) :
    age = serializers.ReadOnlyField() # ajout de la propriété age

    class Meta :
        model = User
        fields = ["id", "username","email", "password", "birth_date","can_be_contacted", "can_data_be_shared", "age"] # listes des champs exposer via l'API
        extra_kwargs = {"password" : {"write_only": True}} # Assure que le mot de passe n'est jamais renvoyer en clair

    def validate_birth_date(self, value):
        "Validation RGPD : L'utilisateur doit avoir plus de 15 ans"
        if value is None:
            raise serializers.ValidationError(
                "La date de naissance est obligatoire pour verifier l'age"
            )
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15 :
                raise serializers.ValidationError ("Vous devez avoir plus de 15 ans pour vous inscrire.")
        return value
        
    def create (self, validated_data) :
        "Surcharge de la methode create pour hacher le mot de passe"
        user = User.objects.create_user(**validated_data)
        return user