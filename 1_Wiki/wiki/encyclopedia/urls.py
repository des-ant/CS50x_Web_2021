from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Pass title to wiki function to read markdown file
    path("wiki/<str:title>", views.wiki, name="wiki")
]
