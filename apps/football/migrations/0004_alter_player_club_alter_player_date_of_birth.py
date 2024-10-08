# Generated by Django 4.2.13 on 2024-08-18 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0003_alter_league_short_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='football.club', verbose_name='Club'),
        ),
        migrations.AlterField(
            model_name='player',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
