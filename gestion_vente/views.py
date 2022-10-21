from ast import Delete
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion_vente import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from gestion_vente.magasin import Client, Magasin, Order
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
    #models.Produit.objects.create(typeProduit="fruit legume",nomProduit="Pomme Vert 500g", prixUnitair=2.99,lienPhoto="/static/imgs/connexion.png")
    # models.Produit.objects.create(typeProduit="fruit legume",nomProduit="ail 200g", prixUnitair=0.99,lienPhoto="/static/imgs/ail.jpg") 

    # models.Produit.objects.create(typeProduit="fruit legume",nomProduit="banane 2000g", prixUnitair=3.99,lienPhoto="/static/imgs/banane.jpg") 

    # models.Produit.objects.create(typeProduit="fruit legume",nomProduit="ciboulette 200g", prixUnitair=1.99,lienPhoto="/static/imgs/ciboulette.jpg") 

    # models.Produit.objects.create(typeProduit="fruit legume",nomProduit="laitue 500g", prixUnitair=1.99,lienPhoto="/static/imgs/laitue.jpg") 

    # models.Produit.objects.create(typeProduit="fruit legume",nomProduit="oignon 2000g", prixUnitair=3.99,lienPhoto="/static/imgs/oignon.jpg") 

    # models.Produit.objects.create(typeProduit="fruit legume",nomProduit="patate 2000g", prixUnitair=2.99,lienPhoto="/static/imgs/patate.jpg") 

    # models.Produit.objects.create(typeProduit="pain",nomProduit="bagel 450g", prixUnitair=1.99,lienPhoto="/static/imgs/bagel.jpg") 

    # models.Produit.objects.create(typeProduit="pain",nomProduit="pain 675g", prixUnitair=2.55,lienPhoto="/static/imgs/pain.jpg") 

    # models.Produit.objects.create(typeProduit="pain",nomProduit="tortillas 1000g", prixUnitair=4.55,lienPhoto="/static/imgs/tortillas.jpg") 

    # models.Produit.objects.create(typeProduit="produit laitier et oeufs",nomProduit="beurre 600g", prixUnitair=4.99,lienPhoto="/static/imgs/beurre.jpg") 

    # models.Produit.objects.create(typeProduit="produit laitier et oeufs",nomProduit="creme 600g", prixUnitair=3.99,lienPhoto="/static/imgs/creme.jpg") 

    # models.Produit.objects.create(typeProduit="produit laitier et oeufs",nomProduit="fromage 450g", prixUnitair=5.99,lienPhoto="/static/imgs/fromage.jpg") 

    # models.Produit.objects.create(typeProduit="produit laitier et oeufs",nomProduit="oeufs 30", prixUnitair=7.99,lienPhoto="/static/imgs/oeufs.jpg") 

    # models.Produit.objects.create(typeProduit="produit laitier et oeufs",nomProduit="pecorino 400g", prixUnitair=6.99,lienPhoto="/static/imgs/pecorino.jpg") 

    # models.Produit.objects.create(typeProduit="surgelés",nomProduit="dumpling 1000g", prixUnitair=9.99,lienPhoto="/static/imgs/dumpling.jpg") 

    # models.Produit.objects.create(typeProduit="surgelés",nomProduit="glace_chocolat 500g", prixUnitair=3.99,lienPhoto="/static/imgs/glace_chocolat.jpg") 

    # models.Produit.objects.create(typeProduit="surgelés",nomProduit="glace_vanille 500g", prixUnitair=3.99,lienPhoto="/static/imgs/glace_vanille.jpg") 

    # models.Produit.objects.create(typeProduit="surgelés",nomProduit="pizza 600g", prixUnitair=10.99,lienPhoto="/static/imgs/pizza.jpg") 

    # models.Produit.objects.create(typeProduit="viande",nomProduit="boeuf 1000g", prixUnitair=8.99,lienPhoto="/static/imgs/boeuf.jpg") 

    # models.Produit.objects.create(typeProduit="viande",nomProduit="porc 1000g", prixUnitair=4.99,lienPhoto="/static/imgs/porc.jpg") 

    # models.Produit.objects.create(typeProduit="viande",nomProduit="poulet 1500g", prixUnitair=9.99,lienPhoto="/static/imgs/poulet.jpg") 

    # models.Produit.objects.create(typeProduit="autres",nomProduit="chocolat", prixUnitair=2.99,lienPhoto="/static/imgs/chocolat.jpg") 

    # models.Produit.objects.create(typeProduit="autres",nomProduit="pate_rigatoni 1000g", prixUnitair=1.99,lienPhoto="/static/imgs/pate_rigatoni.jpg") 

    # models.Produit.objects.create(typeProduit="autres",nomProduit="poivre 200g", prixUnitair=3.99,lienPhoto="/static/imgs/poivre.jpg") 

    # models.Produit.objects.create(typeProduit="autres",nomProduit="sel 500g", prixUnitair=0.99,lienPhoto="/static/imgs/sel.jpg") 

    # models.Produit.objects.create(typeProduit="autres",nomProduit="sucre_glace 300g", prixUnitair=2.99,lienPhoto="/static/imgs/sucre_glace.jpg") 
    
    listeProduit = models.Produit.objects.all()
    return render(request, "produit_liste.html", {"listeProduit":listeProduit} )

def produit_delete(request,nid):
    models.Produit.objects.filter(id=nid).delete()
    return redirect("/produit/liste")

class produitModelForm(forms.ModelForm):

    class Meta:
        model = models.Produit
        fields = "__all__"
        
def produit_edite(request,nid):
    pass