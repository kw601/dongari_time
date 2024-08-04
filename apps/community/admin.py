from django.contrib import admin
from apps.community import models
# Register your models here.

admin.site.register(models.Club)
admin.site.register(models.Board)
admin.site.register(models.Post)
admin.site.register(models.Comment)