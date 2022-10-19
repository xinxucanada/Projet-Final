from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion_vente import models
from django import forms


def home(request):
    return HttpResponse("Hello, Django!")
# Create your views here.


class CompteModelForm(forms.ModelForm):

    # nomCompte = forms.CharField(min_length=4, label="Nom Compte")

    class Meta:
        form = models.CompteUser()
        fields = ["nomCompte", "nom", "prenom", "telephone", "courriel", "motDePasse", "dateNaissance", "gender"]
        # widgets = {
        #     "motDePasse": forms.PasswordInput(), 
        # }

def compte_creer(request):

    # if request.method == "GET":
    #     form = CompteModelForm()
    #     return render(request, "compte_creer.html", {"form":form})

    # form = CompteModelForm(data=request.POST)
    # if form.is_valid():
    #     form.save()
    #     return HttpResponse("Compte creer success")
    # else:
    #     return render(request, "compte_creer.html", {"form":form})
