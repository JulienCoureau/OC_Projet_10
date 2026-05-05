from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User (AbstractUser) :
    birth_date = models.DateField(null= True , blank = True) # stock la date de naissance, verifie l'age (RGPD)
    can_be_contacted = models.BooleanField(default= False) # choix de confidentialité
    can_data_be_shared = models.BooleanField(default = False)

    @property
    def age (self) : 
        """ Calcule l'age de l'utilisateur à partir de sa date de naissance"""
        if not self.birth_date :
            return 0
        today = date.today()
        return today.year - self.birth_date.year - (
        (today.month, today.day) < (self.birth_date.month, self. birth_date.day)
        )

    