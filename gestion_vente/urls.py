from django.urls import path
from gestion_vente import views

urlpatterns = [
    path("", views.home, name="home"),
]