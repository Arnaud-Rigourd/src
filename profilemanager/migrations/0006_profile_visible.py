# Generated by Django 4.2.1 on 2023-05-17 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilemanager', '0005_rename_project_url_projects_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
