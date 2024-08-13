from django.urls import path,include 
from .views import *
#from django.contrib.auth import views as auth_views
from . import views

app_name = "landing"

urlpatterns = [
    path("", main, name="main"),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("delete/<int:id>/", delete, name="delete"),
    path("update/",update, name="update"),
    path('change_password/',change_password, name="change_password"),
    path("club_auth/", club_auth, name="club_auth"),

    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset_form'),
    #path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    #path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    #path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

