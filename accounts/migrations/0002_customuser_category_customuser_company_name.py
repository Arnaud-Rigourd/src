# Generated by Django 4.2.1 on 2023-05-16 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='category',
            field=models.CharField(choices=[('developpeur', 'Développeur'), ('entrepreneur', 'Entrepreneur')], default='developpeur', max_length=250),
        ),
        migrations.AddField(
            model_name='customuser',
            name='company_name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
