# Generated by Django 4.2.1 on 2023-05-17 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilemanager', '0007_alter_projects_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='link',
            field=models.URLField(blank=True, default=''),
        ),
    ]
