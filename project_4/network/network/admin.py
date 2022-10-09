from django.contrib import admin

from .models import User, Posts, Follow

# Design
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "password")

class PostsAdmin(admin.ModelAdmin):
    list_display = ("id", "user_post", "content_post", "timestamp")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Follow)

