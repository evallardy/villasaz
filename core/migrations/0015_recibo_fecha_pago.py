# Generated by Django 4.0.4 on 2022-05-31 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_matto_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibo',
            name='fecha_pago',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='FecahPago'),
        ),
    ]
