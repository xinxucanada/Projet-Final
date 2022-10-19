from django.urls import path
from gestion_vente import views

urlpatterns = [
    path("", views.home, name="home"),
    path("compte/creer/", views.compte_creer, name="compte_creer"),
    path("compte/liste/", views.compte_liste, name="compte_liste"),
    path("adresse/<int:nid>/creer/", views.adresse_creer, name="adresse_creer"),
]