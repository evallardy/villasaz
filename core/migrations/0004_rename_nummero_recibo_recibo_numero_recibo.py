# Generated by Django 4.0.4 on 2022-05-28 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_recibo_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recibo',
            old_name='nummero_recibo',
            new_name='numero_recibo',
        ),
    ]
