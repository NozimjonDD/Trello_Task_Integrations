# Generated by Django 4.2.13 on 2024-08-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0006_alter_team_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('draft', 'Draft')], default='draft', max_length=100),
        ),
    ]
