# Generated by Django 4.2 on 2025-01-07 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productquality'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductQuality',
        ),
    ]