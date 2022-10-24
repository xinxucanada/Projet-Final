from gestion_vente import models

# class Produit_chose:

#     def __init__(self,id, qty) -> None:
#         self.id = id
#         self.qty = qty

#     def __str__(self) -> str:
#         return f"{self.id},{self.qty}"

class Panier:
    
    def __init__(self, nom_compte) -> None:
        self.nom_compte = nom_compte
        self.dico = {"nomCompte": nom_compte}

    def ajouter(self, produitID, qty):
        self.dico["idProduit"] = produitID
        if models.LignePanier.objects.filter(**self.dico).exists():
            qty += models.LignePanier.objects.filter(**self.dico).first().quantite
            models.LignePanier.objects.filter(**self.dico).update(quantite=qty)
        else:
            models.LignePanier.objects.create(nomCompte=self.nom_compte, idProduit=produitID, quantite=qty)

    # def __add__(self, other):
    #     # p.idClient = self.idClient
    #     for k, v in other.choses.items():
    #         if k in self.choses.keys():
    #             self.choses[k] += v
    #         else:
    #             self.choses[k] = v
    #     other.choses = {}

    # def save(self):
    #     for k, v in self.choses.items():
    #         models.LignePanier.objects.create(nomCompte_id=self.nom_compte, idProduit_id=k, quantite=v)
        

class Order:

    def __init__(self, id_commande) -> None:
        self.commande = models.LigneCommande.objects.filter(idCommande=id_commande)



class Client:

    def __init__(self, nom_compte):
        
        # self.compte = models.CompteUser.objects.filter(nomCompte=nom_compte).first()
        self.compte = nom_compte
        self.panier = Panier(nom_compte)
        self.orders = []
        if models.LignePanier.objects.filter(nomCompte=nom_compte).exists():
            for ligne in models.LignePanier.objects.filter(nomCompte=nom_compte):
                self.panier.choses[ligne.idProduit.id] = ligne.quantite
        if models.Commande.objects.filter(nomCompte=nom_compte).exists():
            for i in models.Commande.objects.filter(nomCompte=nom_compte):
                self.orders.append(Order(i.id))
    def __str__(self) -> str:
        return self.compte

class Magasin:

    def __init__(self): 
        self.client = None
        # self.panier = Panier()
        

    def login(self, nom_compte):
        self.client = Client(nom_compte)




