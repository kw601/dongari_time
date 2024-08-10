from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    club_id = models.ForeignKey("community.Club", null=True, on_delete=models.SET_NULL)
    name = models.CharField("이름", max_length=20, null=False)
    nickname = models.CharField("닉네임", max_length=20, null=False)
    phone_num = models.CharField("전화번호", max_length=20, null=False)
    is_admin = models.BooleanField("동아리장여부", default=False)


class Auth_Club(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    club_id = models.ForeignKey("community.Club", on_delete=models.CASCADE)

    def __str__(self) -> Any:
        return f'"{self.club_id}" 회원 : {self.user_id}'
