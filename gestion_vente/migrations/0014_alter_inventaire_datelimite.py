# Generated by Django 4.1.1 on 2022-10-22 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_vente', '0013_alter_inventaire_numlot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventaire',
            name='dateLimite',
            field=models.DateField(blank=True, default='9999-12-31', null=True, verbose_name='date peremption'),
        ),
    ]
