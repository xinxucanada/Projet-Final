# Generated by Django 4.1.2 on 2022-10-21 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_vente', '0008_remove_lignepanier_prixunitair'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='lienPhoto',
            field=models.CharField(default='', max_length=100, verbose_name='lien photo'),
        ),
        migrations.AddField(
            model_name='produit',
            name='typeProduit',
            field=models.CharField(default='produit', max_length=20, verbose_name='type du produit'),
        ),
    ]
