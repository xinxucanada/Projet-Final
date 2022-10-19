# Generated by Django 4.1.1 on 2022-10-19 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_vente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresseLivre', models.CharField(max_length=100, verbose_name='ville')),
                ('dateCommande', models.DateField(auto_now_add=True, verbose_name='Date de commande')),
                ('motant', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='motant')),
                ('taxe', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='taxe')),
                ('fraisTransport', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='frais de transport')),
                ('idCompte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_vente.compteuser', verbose_name='id compte')),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomProduit', models.CharField(max_length=20, verbose_name='Nom du Produit')),
                ('prixUnitair', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Prix Unitaire')),
                ('inventaire', models.IntegerField(default=0, verbose_name='quantite')),
                ('dateLimite', models.DateField(default='9999-12-31', verbose_name='quantite')),
                ('numLot', models.CharField(max_length=20, verbose_name='numero de lot')),
            ],
        ),
        migrations.CreateModel(
            name='LignePanier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prixUnitair', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Prix Unitaire')),
                ('quantite', models.IntegerField(verbose_name='quantite')),
                ('idCompte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_vente.compteuser', verbose_name='id compte')),
                ('idProduit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_vente.produit', verbose_name='id produit')),
            ],
        ),
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prixUnitair', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Prix Unitaire')),
                ('quantite', models.IntegerField(verbose_name='quantite')),
                ('Produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_vente.produit', verbose_name='produit')),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_vente.commande', verbose_name='id commande')),
            ],
        ),
    ]
