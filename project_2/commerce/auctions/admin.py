from django.contrib import admin

from .models import Category, User, Listing, Comment, Bid, Watchlist

# Design
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "password")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name_of_category",)

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title_of_listing", "time_of_creation")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "price_of_bid", "bid_for_listing", "bid_from_user")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "watchlist_for_listing", "watchlist_from_user")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
