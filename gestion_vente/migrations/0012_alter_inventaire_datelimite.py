# Generated by Django 4.1.1 on 2022-10-22 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_vente', '0011_inventaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventaire',
            name='dateLimite',
            field=models.DateField(default='9999-12-31', verbose_name='date peremption'),
        ),
    ]
