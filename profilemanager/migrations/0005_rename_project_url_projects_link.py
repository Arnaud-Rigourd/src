# Generated by Django 4.2.1 on 2023-05-17 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profilemanager', '0004_alter_profile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projects',
            old_name='project_url',
            new_name='link',
        ),
    ]
