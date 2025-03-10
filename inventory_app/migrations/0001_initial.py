# Generated by Django 5.1.7 on 2025-03-10 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_assigned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_issued', models.DateTimeField(auto_now_add=True)),
                ('date_returned', models.DateTimeField(blank=True, null=True)),
                ('gun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.gun')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.person')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.rank'),
        ),
    ]
