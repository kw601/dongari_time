from django.urls import path
from .views import *

app_name = "community"

urlpatterns = [
    path('board/<int:board_id>/post/<int:post_id>/', post_detail, name='post_detail'),
]
