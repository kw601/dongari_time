# Generated by Django 5.0.7 on 2024-08-05 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_comment_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]