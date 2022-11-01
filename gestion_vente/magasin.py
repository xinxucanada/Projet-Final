from gestion_vente import models
from django.utils.safestring import mark_safe

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
            models.LignePanier.objects.create(nomCompte_id=self.nom_compte, idProduit_id=produitID, quantite=qty)

# surcharger opérateur 
    def __add__(self, other):
        panier_other = models.LignePanier.objects.filter(**other.dico)
        for row in panier_other:
            self.ajouter(row.idProduit_id, row.quantite)
        models.LignePanier.objects.filter(nomCompte_id=other.nom_compte).delete()



class Order:

    def __init__(self, id_commande) -> None:
        self.commande = models.LigneCommande.objects.filter(idCommande=id_commande)



class Client:

    def __init__(self, nom_compte):
        
        self.compte = nom_compte
        # composition
        self.panier = Panier(nom_compte)
        
    def __str__(self) -> str:
        return self.compte

class Magasin:

    def __init__(self): 
        self.client = None
        self.commande_liste = []
        self.message =""
        self.commande_montant = 0
        

    def login(self, nom_compte):
        # aggrégation
        self.client = Client(nom_compte)



class Recette:
    
    def __init__(self) -> None:
        self.nom = ""
        self.photo = ""
        self.video_id = ""
        self.produits = []
        self.preparation = ""

d = Recette()
d.nom = "Gratin Dauphinois"
d.photo = "/static/imgs/dauphinois.png"
d.video_id = "dk1ynZT8BwI"
d.produits = [118, 123, 122, 113]
d.preparation = mark_safe("<ol>"\
                    "<li>Préchauffez le four th. 5 (150 °C). Pelez les pommes de terre et coupez-les en rondelles fines.</li><br>"\
                    "<li>Frottez un plat à gratin avec la gousse d’ail pelée puis beurrez-le. Rangez les pommes de terre en plusieurs couches. Salez et poivrez entre chaque couche.</li><br>"\
                    "<li>Versez la crème, salez et poivrez à nouveau. Parsemez du reste de beurre coupé en morceaux. Enfournez votre gratin dauphinois 1 h 30. Servez très chaud.</li><br>"\
                "</ol>"\
                "<ul>"   \
                    "<li>1,5kg Pommes de terre à chair ferme</li>"\
                    "<li>40cl Crème fraîche liquide</li>"\
                    "<li>50g Beurre</li>"\
                    "<li>1gousse Ail</li>"\
                "</ul>")

r = Recette()
r.nom = "Rigatoni cacio e pepe"
r.photo = "rigatoni.png"
r.video_id = "Af3XXeiWMqU"
r.produits = [135, 126, 137, 136]
r.preparation = mark_safe("<ol>"\
                    "<li>Râpez le pecorino.</li><br>"\
                    "<li>Dans une cocotte, chauffez 4 litres d’eau avec 28 g de sel.</li><br>"\
                    "<li>Lorsque l’eau bout, ajoutez les pâtes en une fois et faites cuire 9 minutes.</li><br>"\
                    "<li>Au bout de 6 minutes, prélevez 10 cl d’eau de cuisson.</li><br>"\
                    "<li>Dans un large poêle, chauffez 10 cl d’eau de cuisson avec le pecorino râpé. Mélangez jusqu’à l’obtention d’une sauce crémeuse.</li><br>"\
                    "<li>Égouttez vos pâtes.</li><br>"\
                    "<li>Ajoutez-les dans la poêle, enrobez-les de sauce et poursuivez la cuisson 2 minutes.</li><br>"\
                    "<li>Poivrez généreusement.</li><br>"\
                "</ol>")

o = Recette()
o.nom = "Oeuf cocotte"
o.photo = "oeuf_cocotte.png"
o.video_id = "u8dDq7eATp0"
o.produits = [125, 123, 122, 115]
o.preparation = mark_safe( "<ol>"\
                    "<li>Préchauffez le four à 200 °C.</li><br>"\
                    "<li>Beurrez 4 ramequins allant au four et ajoutez-y la crème.</li><br>"\
                    "<li>Cassez l’œuf par-dessus, salez puis poivrez.</li><br>"\
                    "<li>Mettez les ramequins dans un plat allant au four rempli d'eau bouillante.</li><br>"\
                    "<li>Enfournez 10 à 15 min environ, selon la cuisson souhaitée.</li><br>"\
                    "<li>Ciselez la ciboulette par-dessus et servez.</li><br>"\
                "</ol>"\
                "<ul>"   \
                    "<li>4 Oeufs</li>"\
                    "<li>15cl Crème fraîche</li>"\
                    "<li>10g Beurre</li>"\
                    "<li>Brins de ciboulette(un peu) </li>"\
                "</ul>")


m = Recette()
m.nom = "Mousse au chocolat"
m.photo = "mousse_chocolat.png"
m.video_id = "3v-EEdxhemE"
m.produits = [134, 125, 122, 138]
m.preparation = mark_safe("<ol>"\
                    "<li>Cassez le chocolat en petits morceaux, faites-le fondre au bain-marie,"\
                    "puis retirez de feu. Ajoutez le beurre en morceaux, mélangez jusqu'à ce qu’il"\
                    "soit bien fondu Ajoutez les jaunes d’œufs, mélangez.</li><br>"\
                    "<li>Montez les blancs en neige ferme, ajoutez le sucre glace à la fin."\
                    "Incorporez les blancs délicatement au chocolat fondu.</li><br>"\
                    "<li>Répartissez la mousse dans 4 coupes individuelles,"\
                    "réservez-les au frais jusqu’au moment de servir.</li><br>"\
                "</ol>"\
                "<ul>"   \
                    "<li>100g Chocolat pâtissier</li>"\
                    "<li>3 Oeufs</li>"\
                    "<li>30g Beurre</li>"\
                    "<li>2cuil. à soupe Sucre glace</li>"\
                "</ul>")

class ListeRecttes:

    def __init__(self) -> None:
        self.liste = [d, r, o , m]



