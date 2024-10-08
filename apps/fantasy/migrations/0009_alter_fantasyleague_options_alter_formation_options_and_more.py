# Generated by Django 4.2.13 on 2024-08-21 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0018_alter_player_position'),
        ('fantasy', '0008_teamplayer_formation_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fantasyleague',
            options={'verbose_name': 'Fantasy league', 'verbose_name_plural': 'Fantasy leagues'},
        ),
        migrations.AlterModelOptions(
            name='formation',
            options={'verbose_name': 'Squad formation', 'verbose_name_plural': 'Squad formations'},
        ),
        migrations.AlterModelOptions(
            name='formationposition',
            options={'verbose_name': 'Squad formation position', 'verbose_name_plural': 'Squad formation positions'},
        ),
        migrations.AlterModelOptions(
            name='leagueparticipant',
            options={'verbose_name': 'Fantasy league participant', 'verbose_name_plural': 'Fantasy league participant'},
        ),
        migrations.AlterModelOptions(
            name='squad',
            options={'verbose_name': 'Squad', 'verbose_name_plural': 'Squads'},
        ),
        migrations.AlterModelOptions(
            name='squadplayer',
            options={'verbose_name': 'Squad player', 'verbose_name_plural': 'Squad players'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'Team', 'verbose_name_plural': 'Teams'},
        ),
        migrations.AlterModelOptions(
            name='teamplayer',
            options={'verbose_name': 'Team player', 'verbose_name_plural': 'Team players'},
        ),
        migrations.AddField(
            model_name='squad',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='Is default squad'),
        ),
        migrations.AlterField(
            model_name='squad',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='football.round', verbose_name='Round'),
        ),
    ]
