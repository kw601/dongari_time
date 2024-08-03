from django.urls import path
from django.shortcuts import render
from .views import *
#from * import views

app_name = "community"

urlpatterns = [
    path("<int:board_id>/", post_list, name="post_list"),
    path("<int:board_id>/post/<int:post_id>/", post_detail, name="post_detail"),
    path("<int:board_id>/create/", create_post, name="create_post"),
]
