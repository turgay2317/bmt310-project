# Generated by Django 3.2.9 on 2024-05-14 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kurumlar',
            name='kurumAktif',
            field=models.BooleanField(default=False),
        ),
    ]
