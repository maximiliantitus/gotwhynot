# Generated by Django 2.2 on 2020-05-17 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20200517_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.CharField(choices=[('Active', 'Active'), ('Sold Out', 'Sold Out')], default='Active', max_length=20),
        ),
    ]
