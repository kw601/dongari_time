from django.urls import path
from django.shortcuts import render
from .views import *
#from * import views

app_name = "community"

urlpatterns = [
    path("<int:board_id>/", post_list, name="post_list"),
    path("<int:board_id>/post/<int:post_id>/", post_detail, name="post_detail"),
    path("<int:board_id>/create/", create_post, name="create_post"),
    path("create_board/", create_board, name="create_board"),
    # path("board_list/", board_list, name="board_list"),
    path("", board_list, name="board_list"),
    path("<int:board_id>/delete/", delete_board, name="delete_board"),
]
