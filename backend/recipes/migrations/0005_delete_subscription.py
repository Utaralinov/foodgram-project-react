# Generated by Django 4.1.3 on 2022-12-03 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_subscription_subscription_unique_subscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
