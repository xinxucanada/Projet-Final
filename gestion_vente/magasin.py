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
        self.panier = Panier()

    def login(self, nom_compte):
        self.client = Client(nom_compte)


class Produit_chose:

    def __init__(self,id, qty) -> None:
        self.id = id
        self.qty = qty

    def __str__(self) -> str:
        return f"{self.id},{self.qty}"

class Panier:
    
    def __init__(self) -> None:
        self.idClient = None
        self.choses = {}

    def ajouter(self, produit, id=None):
        self.idClient = id
        if produit.id in self.choses.keys():
            self.choses[produit.id] += produit.qty
        else:
            self.choses[produit.id] = produit.qty

    def __add__(self, other):
        # p.idClient = self.idClient
        for k, v in other.choses.items():
            if k in self.choses.keys():
                self.choses[k] += v
            else:
                self.choses[k] = v
        other.choses = {}
        