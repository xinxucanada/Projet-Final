from ast import Delete
from pyexpat import model
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion_vente import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from gestion_vente.magasin import Client, Magasin, Order,Produit_chose,Panier
from django.utils.safestring import mark_safe

m = Magasin()

# nav barre change selon le situation de compte connexion
def get_nom():
    nom = '<a href="/compte/login/">se connecter</a>'
    if m.client:
        nom = f'<img src="/static/imgs/connexion.png" alt="">{m.client.compte}</li><ul>\
            <li><a href="">profile</a></li><li><a href="">mes commandes</a></li>\
            <li><a href="/compte/deconnecter/">déconnection</a></li></ul></ul>'
    nom = mark_safe(nom)
    return nom   

def home(request):
    nom = get_nom()
    return render(request, "home1.html", {"nom": nom})
# Create your views here.


class CompteModelForm(forms.ModelForm):

    nomCompte = forms.CharField(min_length=4, label="Nom Compte")
    telephone = forms.CharField(
        label = "telephone",
    # mettons que numero de telephon au canada est 10 chiffres
        validators = [RegexValidator(r'^\d{10}$', 'telephone invalide')]
    )
    class Meta:
        model = models.CompteUser
        fields = ["nomCompte", "nom", "prenom", "telephone", "courriel", "motDePasse", "dateNaissance", "gender"]
        widgets = {
            # change input type a password
            "motDePasse": forms.PasswordInput(), 
        }
        
    def clean_telephone(self):
        txt_telephone = self.cleaned_data["telephone"]
        exists = models.CompteUser.objects.filter(telephone=txt_telephone).exists()
        if exists:
            raise ValidationError("Numero de telephone deja existe")

        return txt_telephone

# verifier si le 'user name' ou telephone ou courriel deja inscrit
    def clean_nomCompte(self):
        txt_nomCompte = self.cleaned_data["nomCompte"]
        exists = models.CompteUser.objects.filter(nomCompte=txt_nomCompte).exists()
        if exists:
            raise ValidationError("Nom du compte deja existe")
        return txt_nomCompte

    def clean_courriel(self):
        txt_courriel = self.cleaned_data["courriel"]
        exists = models.CompteUser.objects.filter(courriel=txt_courriel).exists()
        if exists:
            raise ValidationError("courriel deja existe")
        return txt_courriel
 
    def clean_motDePasse(self):
        txt_motDePasse = self.cleaned_data["motDePasse"]
        if len(txt_motDePasse) < 8:
            raise ValidationError("mot de passe doit avoir plus que 8 chars")

        return txt_motDePasse

def compte_creer(request):

    if request.method == "GET":
        form = CompteModelForm()
        return render(request, "compte_creer.html", {"form":form})

    form = CompteModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        # demander l'utilisateur de creer son adressed des que son compte est cree
        return redirect("/adresse/creer/")
    else:
        return render(request, "compte_creer.html", {"form":form})

class AdresseModelForm(forms.ModelForm):

    class Meta:
        model = models.Adresse
        fields = ('adresse', 'ville', 'codePostale', 'province',)
        
def adresse_creer(request):
    nom = get_nom()
    if request.method == "GET":
        form = AdresseModelForm()
        return render(request, "adresse_creer.html", {"form":form, "nom":nom})

    form = AdresseModelForm(data=request.POST)
    if form.is_valid():
    # comme AdresseModelForm n'a pas compte_id, il faut "save(commit=False)", puis donner id
        new_adresse = form.save(commit=False)
        new_adresse.Compte_id = models.CompteUser.objects.filter(nomCompte=m.client.compte).first().id
        new_adresse.save()
        return redirect("home")
    else:
        return render(request, "adresse_creer.html", {"form":form})

def compte_login(request):
    if request.method == "GET":
        return render(request, 'compte_login.html')
# verifier que le client entre 'user name' ou telephone ou courriel
    data_login = request.POST.get('data_login')
    if models.CompteUser.objects.filter(nomCompte=data_login).exists():
        nom_compte = data_login
    elif models.CompteUser.objects.filter(telephone=data_login).exists():
        nom_compte = models.CompteUser.objects.filter(telephone=data_login).first().nomCompte
    elif models.CompteUser.objects.filter(courriel=data_login).exists():
        nom_compte = models.CompteUser.objects.filter(courriel=data_login).first().nomCompte
    else:
        msg_error = 'Compte n\'existe pas!!'
        return render(request, 'compte_login.html', {"msg_error": msg_error})
    pwd = request.POST.get('pwd') 
    if pwd == models.CompteUser.objects.filter(nomCompte= nom_compte).first().motDePasse:
# creer objet client par fonction login
        m.login(nom_compte)
        return redirect('home')
    else:
        msg_error = 'Mot de pass incorrect!!'
        return render(request, 'compte_login.html', {"msg_error": msg_error})

def compte_deconnecter(request):
    m.client = None
    return redirect('home')


# class LignePanierModelForm(forms.ModelForm):
#     idProduit_id = forms.IntegerField(disabled=True, label='Produit')
#     class Meta:
#         model = models.LignePanier
#         fields = ("idProduit_id", "quantite")

def compte_panier(request):
    nom = get_nom()
    data_dict = {}
    # mettre toutes les conditions dans un dico, comme nom du compte
    data_dict["nomCompte"] = m.client.compte
    # liste = models.LignePanier.objects.filter(**data_dict)
    liste_panier = models.LignePanier.objects.filter(**data_dict)
    liste = []
    montant = 0
    for obj in liste_panier:
        # avec 'foreignKey' fonctin, on peut avoir lienPhoto et prixUnitair
        photo = mark_safe(f'<img src="{obj.idProduit.lienPhoto}" alt="" style="width:20px;height:20px;">')
        line = [photo, obj.idProduit, obj.quantite, obj.idProduit.prixUnitair, obj.quantite*obj.idProduit.prixUnitair, obj.id]
        liste.append(line)
        montant += obj.quantite * obj.idProduit.prixUnitair
    if request.method == "GET":
        return render(request, "compte_panier.html", {"liste": liste, "nom": nom})
    for obj in liste:
    # si client changer la quantite, update la base de donnee
        if request.POST.get(str(obj[1])):
            quantite_n = int(request.POST.get(str(obj[1])))
            data_dict["idProduit"] = obj[1]
            models.LignePanier.objects.filter(**data_dict).update(quantite=quantite_n)
    return redirect("/compte/panier/")

def panier_delete(request, nid):
    data_dict = {}
    data_dict["nomCompte"] = m.client.compte
    data_dict["id"] = nid
    models.LignePanier.objects.filter(**data_dict).delete()
    return redirect("/compte/panier/")

def compte_commander(request):
    nom = get_nom()
    data_dict = {}
    data_dict["nomCompte"] = m.client.compte
    liste_panier = models.LignePanier.objects.filter(**data_dict)
    liste = []
    montant = 0
    # puisque la base de donnee 'ligne panier n'a pas d'attributs photo, prix, subtotal et montant total no plus'
    # on cree une liste pour afficher toutes les informations
    for obj in liste_panier:
        # avec 'foreignKey' fonctin, on peut avoir lienPhoto et prixUnitair
        photo = mark_safe(f'<img src="{obj.idProduit.lienPhoto}" alt="" style="width:20px;height:20px;">')
        line = [photo, obj.idProduit, obj.quantite, obj.idProduit.prixUnitair, obj.quantite*obj.idProduit.prixUnitair]
        liste.append(line)
        montant += obj.quantite*obj.idProduit.prixUnitair
    return render(request, "compte_commander.html", {"liste": liste, "nom": nom, "montant":montant})

def caisse(request):
    pass    

def shopping(request):
    nom = get_nom()   
    liste = models.Produit.objects.all()
    if request.method == "GET":
        return render(request, "shopping.html", {"liste": liste, "nom":nom})
    for i in range(liste.first().id, liste.last().id + 1):
    # for i in range(113, 139):
        if request.POST.get(str(i)):
            qty = int(request.POST.get(str(i)))
        # qty = int(request.POST.get(i))
        # if qty != 0:
            produit_select = Produit_chose(i, qty)
            # print(produit_select)
            # print(m.client)
            # print(m.client.panier)
            m.client.panier.ajouter(produit_select)
            models.LignePanier.objects.filter(nomCompte=m.client.compte).delete()
            m.client.panier.save()

            return redirect("shopping")

"""
fonctions reservees pour l'administrateur
"""
    
def compte_liste(request):
    liste1 = models.CompteUser.objects.all()
    row = models.CompteUser.objects.filter(id=1).first()
    form = CompteModelForm(instance=row)
    return render(request, "compte_liste.html", {"liste1":liste1, 'form': form})

def compte_delete(request, nid):
    models.CompteUser.objects.filter(id=nid).delete()
    return redirect("/compte/liste")

def produit_liste(request):
    listeProduit = models.Produit.objects.all()
    return render(request, "produit_liste.html", {"listeProduit":listeProduit} )

def produit_delete(request, nid):
    models.Produit.objects.filter(id=nid).delete()
    return redirect("/produit/liste")

class produitModelForm(forms.ModelForm):

    class Meta:
        model = models.Produit
        fields = "__all__"
        
def produit_edit(request, nid):

    row_obj = models.Produit.objects.filter(id=nid).first()
    if request.method == "GET":
        form = produitModelForm(instance=row_obj)
        return render(request, "produit_edit.html", {"form": form})
    
    form = produitModelForm(data=request.POST, instance=row_obj) 
    if form.is_valid():
        form.save()
        return redirect("/produit/liste/")
    else:
        return render(request, "produit_edit.html", {"form":form})

def inventaire_liste(request):
     
    inventaires = models.Inventaire.objects.all().order_by("dateLimite").order_by("idProduit")
    return render(request, "inventaire_liste.html", {"liste":inventaires} )

def inventaire_delete(request, nid):
    models.Inventaire.objects.filter(id=nid).delete()
    return redirect("/inventaire/liste")

class inventaireModelForm(forms.ModelForm):

    class Meta:
        model = models.Inventaire
        fields = "__all__"

def inventaire_edit(request, nid):
    row_obj = models.Inventaire.objects.filter(id=nid).first()
    if request.method == "GET":
        form = inventaireModelForm(instance=row_obj)
        return render(request, "inventaire_edit.html", {"form": form})
    form = inventaireModelForm(data=request.POST, instance=row_obj) 
    if form.is_valid():
        form.save()
        return redirect("/inventaire/liste/")
    else:
        return render(request, "inventaire_edit.html", {"form":form})

# afficher toutes les lignes de panier
def liste_ligne_panier(request):
    liste = models.LignePanier.objects.all()
    return render(request, "liste_panier.html", {"liste": liste})

