from django.urls import path
from .views import *
#from * import views

app_name = "community"

urlpatterns = [
    path('board/<int:board_id>/post/<int:post_id>/', post_detail, name='post_detail'),
    path('board/<int:board_id>/create/', create_post, name='create_post'),
    #path('create/', create_post, name='create_post'),
]
