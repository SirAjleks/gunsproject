# Generated by Django 5.1.7 on 2025-03-10 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0003_person_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='requested',
            field=models.BooleanField(default=False),
        ),
    ]
