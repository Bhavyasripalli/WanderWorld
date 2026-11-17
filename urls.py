from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="social/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("post/create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("user/<str:username>/", views.profile_view, name="profile"),
    path("user/<str:username>/follow/", views.toggle_follow, name="toggle_follow"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("search/", views.search_view, name="search"),
]
