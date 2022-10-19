from operator import mod
from random import choices
from tabnanny import verbose
from django.db import models

# Create your models here.

class CompteUser(models.Model):

    nomCompte = models.CharField(verbose_name='Nom Compte', max_length=20)
    nom = models.CharField(verbose_name='Nom', max_length=20)
    prenom = models.CharField(verbose_name='Prenom', max_length=20)
    telephone = models.CharField(verbose_name='Telephone', max_length=20)
    courriel = models.EmailField(verbose_name='courriel')
    motDePasse = models.CharField(verbose_name='Mot de passe', max_length=30)
    dateNaissance = models.DateField(verbose_name='Date de naissance', null=True, blank=True)
    gender_choices = (
        (1, 'Homme'),
        (2, 'Femme'),
    )
    gender = models.SmallIntegerField(verbose_name='Sexe', choices=gender_choices,null=True, blank=True)


class Adresse(models.Model):

    idCompte = models.ForeignKey(verbose_name='id compte',to="CompteUser", to_field="id",on_delete= models.CASCADE)
    adresse = models.CharField(verbose_name='adresse', max_length=50)
    ville = models.CharField(verbose_name='ville', max_length=20)
    codePostale = models.CharField(verbose_name='code postale', max_length=7)
    province_choix = [
        ('QC', 'Quebec'),
        ('ON', 'Ontario'),
        ('BC', 'Colombie-Britanique'),
        ('AB', 'Alberta'),
        ('PE', 'Île-du-Prince-Édouard'),
        ('MB', 'Manitoba'),
        ('NB', 'Nouveau-Brunswick'),
        ('NS', 'Nouvelle-Écosse'),
        ('SK', 'Saskatchewan'),
        ('NL', 'Terre-Neuve-et-Labrador'),
        ('NU', 'Nunavut'),
        ('NT', 'Territoires du Nord-Ouest'),
        ('YT', 'Yukon'),
    ]
    province = models.CharField(verbose_name='province', max_length=2, choices=province_choix)