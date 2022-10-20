import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion_vente import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from gestion_vente.magasin import Client, Magasin, Order

m = Magasin()


def home(request):
    # nom = 'se connecter'
    if m.client:
        nom = "Bonjour " + m.client.compte.prenom + " " + m.client.compte.nom
        return render(request, "home1.html", {"nom": nom})
    return render(request, "home.html")
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
    

