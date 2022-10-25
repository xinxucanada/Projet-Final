from email.policy import default
from operator import mod
from random import choices
from statistics import mode
from tabnanny import verbose
from django.db import models

# Create your models here.

class CompteUser(models.Model):

    nomCompte = models.CharField(verbose_name='Nom Compte',max_length=20, unique=True)
    nom = models.CharField(verbose_name='Nom',  max_length=20)
    prenom = models.CharField(verbose_name='Prenom', max_length=20)
    telephone = models.CharField(verbose_name='Telephone', max_length=20)
    courriel = models.EmailField(verbose_name='courriel')
    motDePasse = models.CharField(verbose_name='Mot de passe',  max_length=30)
    dateNaissance = models.DateField(verbose_name='Date de naissance', null=True, blank=True)
    gender_choices = (
        (1, 'Homme'),
        (2, 'Femme'),
    )
    gender = models.SmallIntegerField(verbose_name='Sexe', choices=gender_choices,null=True, blank=True)

    def __str__(self) -> str:
        return self.nomCompte


class Adresse(models.Model):

    Compte = models.ForeignKey(verbose_name='ID compte', to="CompteUser", to_field="id", on_delete=models.CASCADE)
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
    province = models.CharField(verbose_name='province', max_length=3, choices=province_choix)

    def __str__(self) -> str:
        return self.adresse + self.ville + self.province + self.codePostale

class Produit(models.Model):

    nomProduit = models.CharField(verbose_name='Nom du Produit', max_length=20)
    typeProduit = models.CharField(verbose_name='type du produit', max_length=20, default="produit")
    prixUnitair = models.DecimalField(verbose_name="Prix Unitaire", max_digits=10, decimal_places=2, default=0)
    # inventaire = models.IntegerField(verbose_name="quantite",default=0)
    # dateLimite = models.DateField(verbose_name="quantite",default='9999-12-31')
    # numLot = models.CharField(verbose_name='numero de lot', max_length=20)
    lienPhoto = models.CharField(verbose_name='lien photo', max_length=100, default="")

    def __str__(self) -> str:
        return self.nomProduit

class Inventaire(models.Model):

    idProduit = models.ForeignKey(verbose_name="id produit", to="Produit", to_field="id", on_delete=models.CASCADE)
    inventaire = models.IntegerField(verbose_name="quantite",default=0)
    dateLimite = models.DateField(verbose_name="date peremption",default='9999-12-31', null=True, blank=True)
    numLot = models.CharField(verbose_name='numero de lot', max_length=20, null=True, blank=True)


class LignePanier(models.Model):

    nomCompte = models.ForeignKey(verbose_name='id compte',to="CompteUser", to_field="nomCompte",on_delete= models.CASCADE)
    idProduit = models.ForeignKey(verbose_name='id produit',to="Produit", to_field="id",on_delete= models.CASCADE)
    # prixUnitair = models.DecimalField(verbose_name="Prix Unitaire", max_digits=10, decimal_places=2, default=0)
    quantite = models.IntegerField(verbose_name="quantite")


class Commande(models.Model):

    nomCompte = models.ForeignKey(verbose_name='id compte',to="CompteUser", to_field="nomCompte",on_delete= models.CASCADE)
    adresseLivre = models.CharField(verbose_name='ville', max_length=100)
    dateCommande = models.DateField(verbose_name='Date de commande', auto_now_add=True)
    motant = models.DecimalField(verbose_name="motant", max_digits=10, decimal_places=2)
    taxe = models.DecimalField(verbose_name="taxe", max_digits=10, decimal_places=2)
    fraisTransport = models.DecimalField(verbose_name="frais de transport", max_digits=10, decimal_places=2)


class LigneCommande(models.Model):

    idCommande = models.ForeignKey(verbose_name='id commande',to="Commande", to_field="id",on_delete= models.CASCADE)
    Produit = models.ForeignKey(verbose_name='produit',to="Produit", to_field="id",on_delete= models.CASCADE)
    prixUnitair = models.DecimalField(verbose_name="Prix Unitaire", max_digits=10, decimal_places=2, default=0)
    quantite = models.IntegerField(verbose_name="quantite")





