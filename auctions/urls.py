from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("categories", views.category, name="category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("addwatch/<int:id>", views.addwatch, name="addwatch"),
    path("removewatch/<int:id>", views.removewatch, name="removewatch"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("closebid/<int:id>", views.closebid, name="closebid"),
    path("closedauctions", views.displayclosed, name="closedauctions"),
]
