# Generated by Django 3.2 on 2021-11-17 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('string_manipulation', '0002_operationmodel_string'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operationmodel',
            old_name='string',
            new_name='string_id',
        ),
    ]
