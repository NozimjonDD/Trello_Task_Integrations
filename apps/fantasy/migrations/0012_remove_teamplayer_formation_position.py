# Generated by Django 4.2.13 on 2024-08-21 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0011_squadplayer_is_captain_squadplayer_is_substitution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamplayer',
            name='formation_position',
        ),
    ]
