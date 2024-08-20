# Generated by Django 4.2.13 on 2024-08-20 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0017_club_league'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='players', to='football.position'),
        ),
    ]
