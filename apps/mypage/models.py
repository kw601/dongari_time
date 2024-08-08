from django.db import models

# Create your models here.

class Scrap(models.Model):
    user_id = models.ForeignKey('landing.User', null=True, on_delete=models.SET_NULL)
    post_id = models.ForeignKey('community.Post', null=True, on_delete=models.SET_NULL)

