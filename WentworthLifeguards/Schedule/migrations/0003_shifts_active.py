# Generated by Django 2.0.3 on 2018-03-27 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0002_auto_20180324_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='shifts',
            name='Active',
            field=models.BooleanField(default=False),
        ),
    ]
