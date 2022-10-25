from django.urls import path
from gestion_vente import views

urlpatterns = [
    path("", views.home, name="home"),
    path("compte/creer/", views.compte_creer, name="compte_creer"),
    path("compte/liste/", views.compte_liste, name="compte_liste"),
    path("compte/login/", views.compte_login, name="compte_login"),
    path("compte/panier/", views.compte_panier, name="compte_panier"),
    path("compte/shopping/", views.shopping, name="shopping"),
    path("compte/deconnecter/", views.compte_deconnecter, name="compte_deconnecter"),
    path("compte/<int:nid>/delete/", views.compte_delete, name="compte_delete"),
    path("compte/commander/", views.compte_commander, name="compte_commander"),
    path("adresse/creer/", views.adresse_creer, name="adresse_creer"),
    path("produit/<int:nid>/delete/", views.produit_delete, name="produit_delete"),
    path("produit/<int:nid>/edit/", views.produit_edit, name="produit_edit"),
    path("produit/liste/", views.produit_liste, name="produit_liste"),
    path("panier/liste/", views.liste_ligne_panier, name="liste_ligne_panier"),
    path("inventaire/liste/", views.inventaire_liste, name="inventaire_liste"),
    path("inventaire/<int:nid>/delete/", views.inventaire_delete, name="inventaire_delete"),
    path("linge_panier/<int:nid>/delete/", views.panier_delete, name="panier_delete"),
    path("inventaire/<int:nid>/edit/", views.inventaire_edit, name="inventaire_edit"),
    path("compte/caisse/", views.compte_caisse, name="compte_caisse"),
    path("compte/info/", views.compte_info, name="compte_info"),



]