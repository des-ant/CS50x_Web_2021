from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing/", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/watch", views.watch, name="watch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("listing/<int:listing_id>/close", views.close_listing, name="close_listing")
]

# Make image url accessible
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)