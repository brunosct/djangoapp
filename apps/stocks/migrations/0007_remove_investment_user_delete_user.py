# Generated by Django 4.2.19 on 2025-02-21 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_alter_investment_total_investment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='user',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
