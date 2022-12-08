from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from . import views

#from django.contrib.auth import views as auth_views #import this

urlpatterns = [
    path("", views.PropertyListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_property", views.create, name="create"),
    path("portfolio", views.portfolio, name="portfolio"),
    path("property/<int:property_id>", views.property, name="property"),
    #path("sales", views.PropertyListViewSales.as_view(), name="sales"), #
    #path("rent", views.PropertyListViewRent.as_view(), name="rent"), #

    # Reset Password
    path("password_reset", views.password_reset, name="password_reset"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)