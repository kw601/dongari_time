from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    club_id = models.ForeignKey('community.Club', null=True, on_delete=models.SET_NULL)
    name = models.CharField("이름", max_length=20, null=False)
    nickname = models.CharField("닉네임", max_length=20, null=False)
    phone_num = models.CharField("전화번호", max_length=20, null=False)
    is_admin =  models.BooleanField("동아리장여부", default=False)