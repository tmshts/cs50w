
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    # API Routes
    path("create_post", views.create_post, name="create_post"),
    path("profil/<str:username>", views.profil, name="profil"),
    path("post/<int:id>", views.post, name="post"),
    path("likes/<int:id>", views.likes, name="likes"),
    path("following", views.following, name="following"),
]
