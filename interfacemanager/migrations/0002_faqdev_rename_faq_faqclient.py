# Generated by Django 4.2.1 on 2023-05-16 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interfacemanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQDev',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='FAQ',
            new_name='FAQClient',
        ),
    ]
