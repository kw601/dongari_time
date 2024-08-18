from django.urls import path
from django.shortcuts import render
from .views import *

# from * import views

app_name = "community"

urlpatterns = [
    path("<int:board_id>/", post_list, name="post_list"),
    path("<int:board_id>/post/<int:post_id>/", post_detail, name="post_detail"),
    path("<int:board_id>/create/", create_post, name="create_post"),
    path("create_board/", create_board, name="create_board"),
    path("", main, name="main"),
    path("<int:board_id>/delete/", delete_board, name="delete_board"),
    path("create_club/", create_club, name="create_club"),
    path("select_club/", select_club, name="select_club"),
    path("post/<int:post_id>/scrap/", scrap_post, name="scrap_post"),
    path("post/<int:post_id>/like/", like_post, name="like_post"),
    path(
        "<int:board_id>/post/<int:post_id>/create_comment/",
        create_comment,
        name="create_comment",
    ),
    path(
        "<int:board_id>/post/<int:post_id>/toggle_pinned/",
        toggle_pinned,
        name="toggle_pinned",
    ),
    path("post/<int:post_id>/delete/", delete_post, name="delete_post"),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    path("search", search, name="search"),
    path("<int:post_id>/delete_post/", delete_post, name="delete_post"),
]
