# Generated by Django 3.0.5 on 2020-05-17 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_order_tracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Accessories', 'Accessories'), ('Outerwear', 'Outerwear'), ('Sale', 'Sale'), ('Tees', 'Tees'), ('Shirts', 'Shirts'), ('Sweatshirts', 'Sweatshirts'), ('Jackets', 'Jackets'), ('Shoes', 'Shoes'), ('Bottoms', 'Bottoms')], default='Not Started', max_length=200),
        ),
    ]
