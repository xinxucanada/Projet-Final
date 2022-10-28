class Recette:
    
    def __init__(self) -> None:
        self.nom = ""
        self.photo = ""
        self.video_id = ""
        self.produits = []
        self.preparation = ""

d = Recette()
d.nom = "Gratin Dauphinois"
d.photo = "dauphinois.png"
d.video_id = "dk1ynZT8BwI"
d.produits = [118, 123, 122, 113]
d.preparation = "<ol>"\
                    "<li>Préchauffez le four th. 5 (150 °C). Pelez les pommes de terre et coupez-les en rondelles fines.</li><br>"\
                    "<li>Frottez un plat à gratin avec la gousse d’ail pelée puis beurrez-le. Rangez les pommes de terre en plusieurs couches. Salez et poivrez entre chaque couche.</li><br>"\
                    "<li>Versez la crème, salez et poivrez à nouveau. Parsemez du reste de beurre coupé en morceaux. Enfournez votre gratin dauphinois 1 h 30. Servez très chaud.</li><br>"\
                "</ol>"\
                "<ul>"   \
                    "<li>1,5kg Pommes de terre à chair ferme</li>"\
                    "<li>40cl Crème fraîche liquide</li>"\
                    "<li>50g Beurre</li>"\
                    "<li>1gousse Ail</li>"\
                "</ul>"

r = Recette()
r.nom = "Rigatoni cacio e pepe"
r.photo = "rigatoni.png"
r.video_id = "Af3XXeiWMqU"
r.produits = [135, 126, 137, 136]
r.preparation = "<ol>"\
                    "<li>Râpez le pecorino.</li><br>"\
                    "<li>Dans une cocotte, chauffez 4 litres d’eau avec 28 g de sel.</li><br>"\
                    "<li>Lorsque l’eau bout, ajoutez les pâtes en une fois et faites cuire 9 minutes.</li><br>"\
                    "<li>Au bout de 6 minutes, prélevez 10 cl d’eau de cuisson.</li><br>"\
                    "<li>Dans un large poêle, chauffez 10 cl d’eau de cuisson avec le pecorino râpé. Mélangez jusqu’à l’obtention d’une sauce crémeuse.</li><br>"\
                    "<li>Égouttez vos pâtes.</li><br>"\
                    "<li>Ajoutez-les dans la poêle, enrobez-les de sauce et poursuivez la cuisson 2 minutes.</li><br>"\
                    "<li>Poivrez généreusement.</li><br>"\
                "</ol>"\
                "<ul>"   \
                    "<li>400g Pâtes de type rigatoni</li>"\
                    "<li>160g Pecorino</li>"\
                    "<li>28g Sel</li>"\
                    "<li>Poivre</li>"\
                "</ul>"


o = Recette()
o.nom = "Oeuf cocotte"
o.photo = "oeuf_cocotte.png"
o.video_id = "u8dDq7eATp0"
o.produits = [125, 123, 122, 115]
o.preparation = "<ol>"\
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
                "</ul>"


m = Recette()
m.nom = "Mousse au chocolat"
m.photo = "mousse_chocolat.png"
m.video_id = "3v-EEdxhemE"
m.produits = [134, 125, 122, 138]
m.preparation = "<ol>"\
                    "<li>1.	Cassez le chocolat en petits morceaux, faites-le fondre au bain-marie,"\
                    "puis retirez de feu. Ajoutez le beurre en morceaux, mélangez jusqu'à ce qu’il"\
                    "soit bien fondu Ajoutez les jaunes d’œufs, mélangez.</li><br>"\
                    "<li>2.	Montez les blancs en neige ferme, ajoutez le sucre glace à la fin."\
                    "Incorporez les blancs délicatement au chocolat fondu.</li><br>"\
                    "<li>3.	Répartissez la mousse dans 4 coupes individuelles,"\
                    "réservez-les au frais jusqu’au moment de servir.</li><br>"\
                "</ol>"\
                "<ul>"   \
                    "<li>100g Chocolat pâtissier</li>"\
                    "<li>3 Oeufs</li>"\
                    "<li>30g Beurre</li>"\
                    "<li>2cuil. à soupe Sucre glace</li>"\
                "</ul>"

class ListeRecttes:

    def __init__(self) -> None:
        self.liste = [d, r, o , m]


