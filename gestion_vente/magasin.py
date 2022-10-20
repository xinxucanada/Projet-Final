from gestion_vente import models

class Order:

    def __init__(self, id_commande) -> None:
        self.commande = models.LigneCommande.objects.filter(idCommande=id_commande)



class Client:

    def __init__(self, nom_compte):
        
        self.compte = models.CompteUser.objects.filter(nomCompte=nom_compte).first()
        self.panier = []
        self.orders = []
        if models.LignePanier.objects.filter(nomCompte=nom_compte).exists():
            self.panier = models.LignePanier.objects.filter(nomCompte=nom_compte)
        if models.Commande.objects.filter(nomCompte=nom_compte).exists():
            for i in models.Commande.objects.filter(nomCompte=nom_compte):
                self.orders.append(Order(i.id))


class Magasin:

    def __init__(self): 
        self.client = None

    def login(self, nom_compte):
        self.client = Client(nom_compte)