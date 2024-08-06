from django.db import models


# Create your models here.
class Club(models.Model):  # 동아리
    club_name = models.CharField("동아리명", max_length=255)
    club_intro = models.CharField("동아리 소개", max_length=255)
    club_num = models.CharField(
        "동아리 인증 번호", max_length=255, unique=True, null=False
    )

    # 동아리 이름 표시용
    def __str__(self):
        return self.club_name


class Board(models.Model):  # 게시판
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
    board_name = models.CharField("게시판 이름", max_length=255, unique=True)


class Post(models.Model):  # 게시글
    user_id = models.ForeignKey("landing.User", on_delete=models.CASCADE)
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField("게시글 제목", max_length=255)
    content = models.TextField("게시글 내용")
    anonymous = models.BooleanField("익명 여부", default=True)
    created_time = models.DateTimeField("작성 시각", auto_now_add=True)
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):  # 댓글
    user_id = models.ForeignKey("landing.User", on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField("댓글 내용")
    anonymous = models.BooleanField("익명 여부", default=True)
    created_time = models.DateTimeField(auto_now_add=True)
