# Generated by Django 4.2.1 on 2023-05-24 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilemanager', '0011_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
