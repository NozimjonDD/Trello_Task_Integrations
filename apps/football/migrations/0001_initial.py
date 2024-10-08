# Generated by Django 4.2.13 on 2024-08-18 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('remote_id', models.PositiveIntegerField(unique=True, verbose_name='remote id')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('short_name', models.CharField(max_length=50, verbose_name='Short name')),
                ('country_id', models.IntegerField()),
                ('venue_id', models.IntegerField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='football/club/logo/')),
                ('logo_path', models.URLField()),
                ('kit', models.ImageField(blank=True, null=True, upload_to='football/club/kit/')),
                ('founded_year', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'football_club',
            },
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('remote_id', models.PositiveIntegerField(unique=True, verbose_name='remote id')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('short_code', models.CharField(max_length=50, verbose_name='Short code')),
                ('image_path', models.URLField(verbose_name='Image path')),
                ('type', models.CharField(max_length=100, verbose_name='Type')),
                ('sub_type', models.CharField(max_length=100, verbose_name='Sub type')),
                ('category_id', models.IntegerField()),
                ('has_jerseys', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'League',
                'verbose_name_plural': 'Leagues',
                'db_table': 'league',
            },
        ),
        migrations.CreateModel(
            name='MatchState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('remote_id', models.PositiveIntegerField(unique=True, verbose_name='remote id')),
                ('state', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('short_title', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'match_state',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('remote_id', models.PositiveIntegerField(unique=True, verbose_name='remote id')),
                ('name', models.CharField(max_length=200)),
                ('short_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'position',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('remote_id', models.PositiveIntegerField(unique=True, verbose_name='remote id')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Is finished')),
                ('pending', models.BooleanField(default=False, verbose_name='Pending')),
                ('is_current', models.BooleanField(default=False, verbose_name='Is current')),
                ('starting_at', models.DateField(verbose_name='Starting at')),
                ('ending_at', models.DateField(verbose_name='Ending at')),
                ('games_in_current_week', models.BooleanField(default=False, verbose_name='Games in current week')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='football.league', verbose_name='League')),
            ],
            options={
                'db_table': 'season',
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('remote_id', models.PositiveIntegerField(unique=True, verbose_name='remote id')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Is finished')),
                ('is_current', models.BooleanField(default=False, verbose_name='Is current')),
                ('starting_at', models.DateField(verbose_name='Starting at')),
                ('ending_at', models.DateField(verbose_name='Ending at')),
                ('games_in_current_week', models.BooleanField(default=False, verbose_name='Games in current week')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='football.league', verbose_name='League')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='football.season', verbose_name='Season')),
            ],
            options={
                'db_table': 'round',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('remote_id', models.PositiveIntegerField(unique=True, verbose_name='remote id')),
                ('country_id', models.IntegerField()),
                ('nationality_id', models.IntegerField()),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='football/player/profile_picture/')),
                ('profile_picture_path', models.URLField()),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=200)),
                ('common_name', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=50)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('club_contract_until', models.DateField(blank=True, null=True)),
                ('market_value', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='football.club', verbose_name='Club')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='football.position')),
            ],
            options={
                'db_table': 'player',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('remote_id', models.PositiveIntegerField(unique=True, verbose_name='remote id')),
                ('venue_id', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('home_club_score', models.IntegerField()),
                ('away_club_score', models.IntegerField()),
                ('result_info', models.CharField(blank=True, null=True, verbose_name='Result info')),
                ('match_date', models.DateTimeField()),
                ('length', models.IntegerField(blank=True, null=True)),
                ('away_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_matches', to='football.club', verbose_name='Away club')),
                ('home_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_matches', to='football.club', verbose_name='Home club')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='football.round', verbose_name='Round')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='football.season', verbose_name='Season')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='football.matchstate', verbose_name='State')),
            ],
            options={
                'db_table': 'match',
            },
        ),
        migrations.CreateModel(
            name='ClubPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('remote_id', models.PositiveIntegerField(unique=True, verbose_name='remote id')),
                ('transfer_id', models.IntegerField(null=True)),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('is_captain', models.BooleanField(default=False)),
                ('kit_number', models.IntegerField()),
                ('is_current_club', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='club_players', to='football.club', verbose_name='Club')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='club_players', to='football.player')),
            ],
            options={
                'db_table': 'club_player',
            },
        ),
    ]
