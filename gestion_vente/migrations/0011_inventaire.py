# Generated by Django 4.1.2 on 2022-10-21 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_vente', '0010_remove_produit_datelimite_remove_produit_inventaire_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventaire', models.IntegerField(default=0, verbose_name='quantite')),
                ('dateLimite', models.DateField(default='9999-12-31', verbose_name='quantite')),
                ('numLot', models.CharField(max_length=20, verbose_name='numero de lot')),
                ('idProduit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_vente.produit', verbose_name='id produit')),
            ],
        ),
    ]