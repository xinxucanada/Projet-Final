from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion_vente import models
from django import forms


def home(request):
    return HttpResponse("Hello, Django!")
# Create your views here.


class CompteModelForm(forms.ModelForm):

    nomCompte = forms.CharField(min_length=4, label="Nom Compte")

    class Meta:
        model = models.CompteUser
        fields = ["nomCompte", "nom", "prenom", "telephone", "courriel", "motDePasse", "dateNaissance", "gender"]
        widgets = {
            "motDePasse": forms.PasswordInput(), 
        }


def compte_creer(request):

    # models.CompteUser.objects.create(nomCompte='XX001', nom='Xu', prenom='Xin', telephone='5141234567', courriel='fjsd@cmail.com', motDePasse='montreal2022',dateNaissance='1985-5-9', gender=2)
    # models.CompteUser.objects.create(nomCompte='XX002', nom='Legault', prenom='Francois', telephone='5149876543', courriel='abc@cmail.com', motDePasse='quebec6789',dateNaissance='1950-5-29', gender=1)
    # return HttpResponse("Compte creer success")
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


class AdresseModelForm(forms.ModelForm):

    class Meta:
        model = models.Adresse
        fields = ['idCompte', 'adresse', 'ville', 'codePostale', 'province']
        


def adresse_creer(request, nid):
    
    if request.method == "GET":
        form = AdresseModelForm()
        return render(request, "adresse_creer.html", {"form":form})

    form = AdresseModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("Adresse creer success")
    else:
        return render(request, "adresse_creer.html", {"form":form})

    

