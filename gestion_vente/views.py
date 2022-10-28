from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion_vente import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from gestion_vente.magasin import Client, Magasin, Order,Panier, ListeRecttes
from django.utils.safestring import mark_safe

m = Magasin()
panier_visiteur = Panier("VISITEUR")
recettes = ListeRecttes()
# commande_liste = []
# commande_montant = 0
# nav barre change selon le situation de compte connexion
def get_nom():
    nom = '<a href="/compte/login/">se connecter</a></span></li></ul>'
    
    if m.client:
        nom = f'<img src="/static/imgs/connexion.png" alt="">{m.client.compte}</span></li><ul>\
                <li><a href="/compte/info/">profile</a></li><li><a href="/compte/histoire/">mes commandes</a></li>\
                <li><a href="/compte/deconnecter/">déconnection</a></li></ul></ul>'
    nom = mark_safe(nom)
    return nom

def get_nbr():
    nbr = models.LignePanier.objects.filter(nomCompte_id="VISITEUR").count()
    if m.client:
        nbr = models.LignePanier.objects.filter(nomCompte_id=m.client.compte).count()
    return nbr

def home(request):
    nom = get_nom()
    nbr = get_nbr()
    return render(request, "home1.html", {"nom": nom, "nbr": nbr})
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
# citer fonction pour donner la classe à chaque input 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "compte_creer_input", "placeholder": field.label}

# verifier si le 'user name' ou telephone ou courriel deja inscrit        
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
        # demander l'utilisateur de creer son adressed des que son compte est cree
        m.login(request.POST.get("nomCompte"))
        return redirect("/adresse/creer/")
    else:
        return render(request, "compte_creer.html", {"form":form})

# class hirétage
class CompteModifier(CompteModelForm):

    nomCompte = forms.CharField(min_length=4, label="Nom Compte", disabled="disabled")

    def clean_telephone(self):
        txt_telephone = self.cleaned_data["telephone"]
        exists = models.CompteUser.objects.exclude(id=self.instance.pk).filter(telephone=txt_telephone).exists()
        if exists:
            raise ValidationError("Numero de telephone deja existe")
        return txt_telephone
    def clean_nomCompte(self):
        txt_nomCompte = self.cleaned_data["nomCompte"]
        exists = models.CompteUser.objects.exclude(id=self.instance.pk).filter(nomCompte=txt_nomCompte).exists()
        if exists:
            raise ValidationError("Nom du compte deja existe")
        return txt_nomCompte
    def clean_courriel(self):
        txt_courriel = self.cleaned_data["courriel"]
        exists = models.CompteUser.objects.exclude(id=self.instance.pk).filter(courriel=txt_courriel).exists()
        if exists:
            raise ValidationError("courriel deja existe")
        return txt_courriel


def compte_modifer(request):
    nom = get_nom()
    if not m.client:
        return redirect("home")
    else:
        row_obj = models.CompteUser.objects.filter(nomCompte=m.client.compte).first()
        if request.method == "GET":
            form = CompteModifier(instance=row_obj)
            return render(request, "compte_modifier.html", {"form": form, "nom": nom})

        form = CompteModifier(data=request.POST, instance=row_obj) 
        if form.is_valid():
            form.save()
            return redirect("/compte/info/")
        else:
            return render(request, "compte_modifier.html", {"form":form, "nom": nom})

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

def adresse_modifier(request, nid):
    nom = get_nom()
    if not m.client:
        return redirect("home")
    else:
        row_obj = models.Adresse.objects.filter(id=nid).first()
        if request.method == "GET":
            form = AdresseModelForm(instance=row_obj)
            return render(request, "adresse_modifier.html", {"form": form, "nom": nom})

        form = AdresseModelForm(data=request.POST, instance=row_obj) 
        if form.is_valid():
            new_adresse = form.save(commit=False)
            new_adresse.Compte_id = models.CompteUser.objects.filter(nomCompte=m.client.compte).first().id
            new_adresse.save()
            return redirect("/compte/info/")
        else:
            return render(request, "adresse_modifier.html", {"form":form, "nom": nom})

def adresse_delete(request, nid):
    models.Adresse.objects.filter(id=nid).delete()
    return redirect("/compte/info/")

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
# utiliser opérateur '+' pour ajouter les produits du panier visiteur au panier client, puis vider panier visiteur
        m.client.panier + panier_visiteur
        return redirect('home')
    else:
        msg_error = 'Mot de pass incorrect!!'
        return render(request, 'compte_login.html', {"msg_error": msg_error})

def compte_deconnecter(request):
    m.client = None
    return redirect('home')

def compte_info(request):
    if not m.client:
        return redirect("/compte/login/")
    nom = get_nom()
    nbr = get_nbr()
    profile = models.CompteUser.objects.filter(nomCompte=m.client.compte).first()
    adresses = models.Adresse.objects.filter(Compte_id=profile.id)
    
    return render(request, "compte_info.html", {"nom": nom, "nbr": nbr, "profile": profile, "adresses":adresses})

def compte_histoire(request):
    models.Commande.objects.filter(id__lte=3).delete()
    if not m.client:
        return redirect("/compte/login/")
    nom = get_nom()
    nbr = get_nbr()
    histoire_commandes = []
    commandes = models.Commande.objects.filter(nomCompte_id=m.client.compte).order_by("-dateCommande")
    for commande in commandes:
        idCommande = commande.id
        linges_commande = models.LigneCommande.objects.filter(idCommande_id=idCommande)
        affiche_plus = mark_safe(f"<button id='btn' style='display:none'>afficher plus</button> <button id='btnMoins' style='display:none'>afficher moins</button>")
        # lignes = None
        # lignes5 = None
        if len(linges_commande) > 7:
            # lignes = linges_commande[:5]
            affiche_plus = mark_safe(f"<button id='btn'>afficher plus</button> <button id='btnMoins'>afficher moins</button>")
            # lignes5 = linges_commande[5:]
        histoire_commandes.append([commande.dateCommande, commande.adresseLivre, commande.montant, linges_commande, idCommande, affiche_plus])
    return render(request, "compte_histoire.html", {"nom": nom, "nbr": nbr, "commandes": histoire_commandes})

def recommander(request, nid):
    if not m.client:
        return redirect("home")
    ligne_commandes = models.LigneCommande.objects.filter(idCommande_id=nid)
    for ligne in ligne_commandes:
        m.client.panier.ajouter(ligne.produit.id, ligne.quantite)
        # models.LignePanier.objects.create(nomCompte_id=m.client.compte, idProduit=ligne.produit, quantite=ligne.quantite)
    return redirect("/compte/panier/")

def compte_panier(request):
    nom = get_nom()
    nbr = get_nbr()
    data_dict = {}
    # mettre toutes les conditions dans un dico, comme nom du compte
    data_dict["nomCompte"] = m.client.compte if m.client else "VISITEUR"
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
        return render(request, "compte_panier.html", {"liste": liste, "nom": nom, "nbr": nbr})
    for obj in liste:
    # si client changer la quantite, update la base de donnee
        if request.POST.get(str(obj[1])):
            quantite_n = int(request.POST.get(str(obj[1])))
            data_dict["idProduit"] = obj[1]
            models.LignePanier.objects.filter(**data_dict).update(quantite=quantite_n)
    return redirect("/compte/panier/")

def panier_delete(request, nid):
    data_dict = {}
    data_dict["nomCompte"] = m.client.compte if m.client else "VISITEUR"
    data_dict["id"] = nid
    models.LignePanier.objects.filter(**data_dict).delete()
    return redirect("/compte/panier/")

def compte_commander(request):
    global message
    if not m.client:
        return redirect("/compte/login/")
    nom = get_nom()
    data_dict = {}
    data_dict["nomCompte"] = m.client.compte
    liste_panier = models.LignePanier.objects.filter(**data_dict)
    m.commande_liste = []
    m.commande_montant = 0
    # m.message = ""
    profile = models.CompteUser.objects.filter(nomCompte=m.client.compte).first()
    adresses = models.Adresse.objects.filter(Compte_id=profile.id)
    # puisque la base de donnee 'ligne panier n'a pas d'attributs photo, prix, subtotal et montant total no plus'
    # on cree une liste pour afficher toutes les informations
    for obj in liste_panier:
        # avec 'foreignKey' fonctin, on peut avoir lienPhoto et prixUnitair
        photo = mark_safe(f'<img src="{obj.idProduit.lienPhoto}" alt="" style="width:30px;height:30px;">')
        line = [photo, obj.idProduit, obj.quantite, obj.idProduit.prixUnitair, obj.quantite*obj.idProduit.prixUnitair]
        m.commande_liste.append(line)
        m.commande_montant += obj.quantite*obj.idProduit.prixUnitair
    return render(request, "compte_commander.html", {"liste": m.commande_liste, "nom": nom, "montant": m.commande_montant, "adresses": adresses, "message": m.message})

def compte_caisse(request):
    adresse_id = request.POST.get("adr_sel")
    if not adresse_id:
        m.message = "Vous devez choisir une adresse!!"
        return redirect("/compte/commander/")
    else:
        m.message = ""
    adresse = models.Adresse.objects.filter(id=adresse_id).first()
    # print(adresse)
    data_dict = {}
    data_dict["nomCompte"] = m.client.compte
    liste_panier = models.LignePanier.objects.filter(**data_dict)
    for row in liste_panier:
        inventaire_deduct(row.idProduit, row.quantite)
    models.Commande.objects.create(nomCompte_id=m.client.compte, adresseLivre=adresse, montant=m.commande_montant )
    id_commande = models.Commande.objects.filter(nomCompte_id=m.client.compte).last().id
    # liste_panier = models.LignePanier.objects.filter(**data_dict)
    for ligne in m.commande_liste:
        models.LigneCommande.objects.create(idCommande_id=id_commande, produit=ligne[1], prixUnitair=ligne[3], quantite=ligne[2])
    models.LignePanier.objects.filter(**data_dict).delete()
    m.commande_montant = 0
    m.commande_liste = []
    return redirect("home")  

# Utiliser recursion pour inventaire  déduction, de date péremption plus proche à plus loins
def inventaire_deduct(idProduit, quantite):
    row_first = models.Inventaire.objects.filter(idProduit=idProduit).order_by("dateLimite").first()
    quantite_stock = row_first.inventaire
    if quantite_stock > quantite:
        models.Inventaire.objects.filter(id=row_first.id).update(inventaire = quantite_stock-quantite)
    else:
        quantite -= quantite_stock
        models.Inventaire.objects.filter(id=row_first.id).delete()
        inventaire_deduct(idProduit, quantite)

def shopping(request):
    nom = get_nom()
    nbr = get_nbr()
    data_dict = {} 
    type = request.GET.get("type","")
    nomProduit = request.GET.get("nomProduit","")
    if type:
        data_dict["typeProduit"] = type 
    if nomProduit:
        print(nomProduit)
        data_dict["nomProduit__contains"] = nomProduit
    liste = models.Produit.objects.filter(**data_dict)
    contente = {
            "liste": liste, 
            "nom":nom, 
            "nbr": nbr, 
            "type": type,
            "nomProduit": nomProduit
        }
    if request.method == "GET":
        return render(request, "shopping.html", contente)

    for i in range(liste.first().id, liste.last().id + 1):
        if request.POST.get(str(i)):
            qty = int(request.POST.get(str(i)))
            if qty !=0:
                if m.client:
                    m.client.panier.ajouter(i, qty)
                else:
                    panier_visiteur.ajouter(i, qty)
    # return render(request, "shopping.html", contente)
    return redirect("shopping")

def recette(request):
    nom = get_nom()
    nbr = get_nbr()
    if request.method == "get":
        recette_choix = int(request.GET.get("r"))
        liste_ingredients = []
        for ingre in recettes.liste[recette_choix].produits:
            print(ingre)
            ingredient = models.Produit.objects.filter(id=ingre).first()
            print(ingredient.lienPhoto)
            liste_ingredients.append(ingredient)
        print(liste_ingredients)
        content = {
            "recette": recettes.liste[recette_choix],
            "nom": nom,
            "nbr": nbr,
            "liste_ingredients": liste_ingredients,
        }
        # if request.method == "get":
        return render(request, "recette.html", content)
    for ingredient in liste_ingredients:
    # si client changer la quantite, update la base de donnee
        if request.POST.get(str(ingredient.id)):
            quantite_n = int(request.POST.get(str(ingredient.id)))
            models.LignePanier.objects.filter(idProduit=ingredient.id).update(quantite=quantite_n)
    return redirect("/recette/")

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

