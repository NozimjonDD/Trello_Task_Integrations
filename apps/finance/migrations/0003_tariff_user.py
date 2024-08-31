# Generated by Django 4.2.13 on 2024-08-31 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0002_tariffcase_remove_tariff_name_tariff_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tariff', to=settings.AUTH_USER_MODEL),
        ),
    ]
