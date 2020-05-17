# Generated by Django 3.0.2 on 2020-05-15 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residences', '0007_residenceimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='residenceimage',
            name='residence_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='images', to='residences.Residence'),
        ),
    ]
