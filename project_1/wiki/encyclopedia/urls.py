from django.urls import path

from . import views


app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("create_new_entry/", views.new_entry, name="new_entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random_page/", views.random_page, name="random_page"), 
    ]
