# Generated by Django 5.0.1 on 2024-02-15 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PizzaApp', '0007_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('address', models.TextField(max_length=150)),
                ('card_no', models.CharField(max_length=19)),
                ('card_exp', models.DateField(auto_now=True)),
                ('cvv', models.CharField(max_length=3)),
            ],
        ),
    ]
