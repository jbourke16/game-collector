# Generated by Django 5.0.4 on 2024-04-04 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='genres',
            field=models.ManyToManyField(to='main_app.type'),
        ),
    ]
