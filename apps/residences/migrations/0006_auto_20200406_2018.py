# Generated by Django 3.0.2 on 2020-04-06 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residences', '0005_delete_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='residence',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]