# Generated by Django 4.2.1 on 2023-06-05 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingsmanager', '0005_rename_message_messages_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='company',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='dev',
        ),
    ]
