# Generated by Django 4.2.1 on 2023-05-17 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilemanager', '0006_profile_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='link',
            field=models.URLField(default=''),
        ),
    ]
