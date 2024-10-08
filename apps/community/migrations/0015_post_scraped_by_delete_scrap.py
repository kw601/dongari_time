# Generated by Django 5.0.7 on 2024-08-11 14:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0014_alter_scrap_unique_together_remove_scrap_post_id_and_more'),
        ('mypage', '0003_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='scraped_by',
            field=models.ManyToManyField(related_name='scraped_posts', through='mypage.Scrap', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Scrap',
        ),
    ]
