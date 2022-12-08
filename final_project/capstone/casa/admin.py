from django.contrib import admin

from .models import User, Property, PropertyType, SalesRent, Images

# Design
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "company_name", "email", "password")

class PropertyAdmin(admin.ModelAdmin):
    list_display = ("id", "type_of_property", "sales_rent", "price", "time_of_creation")

class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_of_property")

class SalesRentAdmin(admin.ModelAdmin):
    list_display = ("id", "sales_or_rent")

class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "images")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(SalesRent, SalesRentAdmin)
admin.site.register(Images, ImagesAdmin)
