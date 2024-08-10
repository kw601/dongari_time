# Generated by Django 5.0.7 on 2024-08-01 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(max_length=255, verbose_name='동아리명')),
                ('club_intro', models.CharField(max_length=255, verbose_name='동아리 소개')),
                ('club_num', models.CharField(max_length=255, unique=True, verbose_name='동아리 인증 번호')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='댓글 내용')),
                ('anonymous', models.BooleanField(default=True, verbose_name='익명 여부')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='게시글 제목')),
                ('content', models.TextField(verbose_name='게시글 내용')),
                ('anonymous', models.BooleanField(default=True, verbose_name='익명 여부')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='작성 시각')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_name', models.CharField(max_length=255, unique=True, verbose_name='게시판 이름')),
                ('club_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.club')),
            ],
        ),
    ]
