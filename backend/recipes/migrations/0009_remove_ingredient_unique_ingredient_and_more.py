# Generated by Django 4.1.3 on 2022-12-04 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_shoppingcart_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingredient',
            name='unique_ingredient',
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient_name'),
        ),
    ]
