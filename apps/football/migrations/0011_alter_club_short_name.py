# Generated by Django 4.2.13 on 2024-08-19 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0010_club_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='short_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Short name'),
        ),
    ]
