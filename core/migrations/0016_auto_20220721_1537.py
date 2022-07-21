# Generated by Django 3.2.4 on 2022-07-21 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_recibo_fecha_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matto',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_matto', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_recibo', to=settings.AUTH_USER_MODEL),
        ),
    ]
