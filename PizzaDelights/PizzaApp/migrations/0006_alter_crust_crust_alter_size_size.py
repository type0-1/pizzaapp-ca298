# Generated by Django 5.0.1 on 2024-02-15 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PizzaApp', '0005_cheese_crust_sauce_size_pizza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crust',
            name='crust',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='size',
            name='size',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], default=('S', 'Small'), max_length=20),
        ),
    ]
