# Generated by Django 3.0.2 on 2020-05-15 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('residences', '0008_auto_20200515_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='residenceimage',
            old_name='residence_id',
            new_name='residence',
        ),
    ]
