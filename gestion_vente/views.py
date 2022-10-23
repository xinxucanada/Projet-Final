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


def home(request):
    nom = '<a href="compte/login/">se connecter</a>'
    if m.client:
        nom = f'<img src="static/imgs/connexion.png" alt="">{m.client.compte}</li><ul>\
            <li><a href="">profile</a></li><li><a href="">mes commandes</a></li>\
            <li><a href="compte/deconnecter/">déconnection</a></li></ul></ul>'
    nom = mark_safe(nom)   
    return render(request, "home1.html", {"nom": nom})
# Create your views here.


class CompteModelForm(forms.ModelForm):

    nomCompte = forms.CharField(min_length=4, label="Nom Compte")
    telephone = forms.CharField(
        label = "telephone",
        validators = [RegexValidator(r'^\d{10}$', 'telephone invalide')]
    )
    

    class Meta:
        model = models.CompteUser
        fields = ["nomCompte", "nom", "prenom", "telephone", "courriel", "motDePasse", "dateNaissance", "gender"]
        widgets = {
            "motDePasse": forms.PasswordInput(), 
        }
        
    
    def clean_telephone(self):
        txt_telephone = self.cleaned_data["telephone"]
        exists = models.CompteUser.objects.filter(telephone=txt_telephone).exists()
        if exists:
            raise ValidationError("Numero de telephone deja existe")

        return txt_telephone

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
        return HttpResponse("Compte creer success")
    else:
        return render(request, "compte_creer.html", {"form":form})


def compte_liste(request):
    #models.CompteUser.objects.create(nomCompte="example",nom="Bone", prenom="James", telephone="1237894650",courriel="example@gogoe.com",motDePasse="123456", dateNaissance="1985-10-1",gender=1)
    
    liste1 = models.CompteUser.objects.all()
    row = models.CompteUser.objects.filter(id=1).first()
    form = CompteModelForm(instance=row)

    return render(request, "compte_liste.html", {"liste1":liste1, 'form': form})

def compte_delete(request, nid):
    models.CompteUser.objects.filter(id=nid).delete()
    return redirect("/compte/liste")


class AdresseModelForm(forms.ModelForm):

    # idCompte = forms.IntegerField(disabled=True, label="compte")

    class Meta:
        model = models.Adresse
        fields = ('adresse', 'ville', 'codePostale', 'province',)
        


def adresse_creer(request, nid):

    # adressTemp = models.Adresse.objects.create(idCompte=nid, adresse='n/a', ville='n/a', codePostale='X0X0X0',province="QC")
    
    if request.method == "GET":
        form = AdresseModelForm()
        # form = AdresseModelForm(idCompte=nid)
        return render(request, "adresse_creer.html", {"form":form})

    form = AdresseModelForm(data=request.POST)
    if form.is_valid():
        
        new_adresse = form.save(commit=False)
        new_adresse.idCompte = nid
        new_adresse.save()
        return HttpResponse("Adresse creer success")
    else:
        return render(request, "adresse_creer.html", {"form":form})

# class LoginModelForm(forms.ModelForm): 

#     class Meta:
#         model = models.CompteUser
#         fields = ["nomCompte", "telephone", "courriel", "motDePasse"]
#         widgets = {
#             "motDePasse": forms.PasswordInput(), 
#         }


def compte_login(request):
    if request.method == "GET":
        return render(request, 'compte_login.html')
    # form = LoginModelForm(data=request.POST)
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
        m.login(nom_compte)
        return redirect('home')
    else:
        msg_error = 'Mot de pass incorrect!!'
        return render(request, 'compte_login.html', {"msg_error": msg_error})


def compte_deconnecter(request):
    m.client = None
    return redirect('home')


def produit_liste(request):
    # models.Produit.objects.all().delete()
    
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
        # print(form.errors)
        return render(request, "produit_edit.html", {"form":form})

def inventaire_liste(request):
     
    # models.Inventaire.objects.create(idProduit_id=138, inventaire=90, dateLimite="2023-12-12", numLot="AH242357") 

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
        # print(form.errors)
        return render(request, "inventaire_edit.html", {"form":form})

def liste_ligne_panier(request):
    # models.LignePanier.objects.create(nomCompte_id="ABC002", idProduit_id=137, quantite=2)
    liste = models.LignePanier.objects.all()
    return render(request, "liste_panier.html", {"liste": liste})

def compte_panier(request):
    print(m.client)
    print(type(m.client))
    print(m.client.panier)
    print(m.client.panier.choses)
    liste = m.client.panier.choses
   
    return render(request, "compte_panier.html", {"liste": liste})

def shopping(request):
    nom = '<a href="/compte/login/">se connecter</a>'
    if m.client:
        nom = f'<img src="/static/imgs/connexion.png" alt="">{m.client.compte}</li><ul>\
            <li><a href="">profile</a></li><li><a href="">mes commandes</a></li>\
            <li><a href="/compte/deconnecter/">déconnection</a></li></ul></ul>'
    nom = mark_safe(nom)   
    liste = models.Produit.objects.all()
    if request.method == "GET":
        return render(request, "shopping.html", {"liste": liste, "nom":nom})
    # for i in range(liste.first().id, liste.last().id + 1):
    for i in range(113, 139):
        qty = int(request.POST.get(str(i)))
        # qty = int(request.POST.get(i))
        if qty != 0:
            produit_select = Produit_chose(i, qty)
            print(produit_select)
            print(m.client)
            print(m.client.panier)
            m.client.panier.ajouter(produit_select)
            return redirect("shopping")

    
