# Generated by Django 5.0.3 on 2024-03-13 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('YAC', 'AC'), ('NAC', 'NON-AC')], max_length=40),
        ),
    ]
