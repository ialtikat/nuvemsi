# Generated by Django 4.0 on 2022-01-19 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_keyuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyuser',
            name='key',
            field=models.CharField(max_length=128),
        ),
    ]
