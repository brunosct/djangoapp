# Generated by Django 4.2.19 on 2025-02-26 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0014_alter_usuario_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='logo',
            field=models.ImageField(null=True, upload_to='user/logos'),
        ),
    ]
