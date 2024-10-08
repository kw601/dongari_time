# Generated by Django 5.0.7 on 2024-08-09 15:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_post_club_id'),
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auth_Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.club')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
