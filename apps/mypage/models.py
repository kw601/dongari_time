from django.db import models

# Create your models here.

class Scrap(models.Model):
    user_id = models.ForeignKey('landing.User', null=True, on_delete=models.CASCADE, related_name='scraps')
    post_id = models.ForeignKey('community.Post', null=True, on_delete=models.CASCADE, related_name='scraps')
    #created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'post_id')

