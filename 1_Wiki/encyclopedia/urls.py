from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    # Pass title to wiki function to read markdown file
    path("wiki/<str:title>", views.wiki, name="wiki"),
    # Url for random encyclopedia entry
    path("random/", views.random_entry, name="random"),
    # Url for creating new encyclopedia entry
    path("newentry/", views.new_entry, name="newentry"),
    # Url for editing encyclopedia entry
    path("edit/<str:title>", views.edit_entry, name="editentry")
]
