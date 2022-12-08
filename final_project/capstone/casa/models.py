from typing_extensions import Required
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models

# added
from casa.choices import *
from multiselectfield import MultiSelectField
#from django_countries.fields import CountryField

#from django.contrib.auth import get_user_model
#User = get_user_model() 

class User(AbstractUser):
    company_name = models.CharField(max_length=200, blank=True)
    representative = models.CharField(max_length=200, blank=True)
    phonenumber = models.CharField(max_length=20)

class PropertyType(models.Model):
    type_of_property = models.CharField(max_length=100)

class SalesRent(models.Model):
    sales_or_rent = models.CharField(max_length=50)

class Property(models.Model):
    # Provided by user
    amenities = MultiSelectField(choices=AMENITIES_CHOICES,
                                 max_choices=30,
                                 max_length=200,
                                 null=True, blank=True)
    bedroom = models.IntegerField(choices=TOTAL_BEDROOM_CHOICES)   
    bathroom = models.FloatField(choices=TOTAL_BATHROOM_CHOICES)
    size = models.IntegerField()
    type_of_property = models.ForeignKey(PropertyType, blank=False, on_delete=models.SET_NULL, null=True, related_name="what_property")
    sales_rent = models.ForeignKey(SalesRent, blank=False, on_delete=models.SET_NULL, null=True, related_name="SalesOrRent")
    title_of_property = models.CharField(max_length=200)
    street_name = models.CharField(max_length=200)
    street_number = models.IntegerField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    #country = CountryField()
    postal_code = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    description_of_property = models.TextField()
    price = models.IntegerField()
    # blank=False - every listing must have category
    listed_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    # when the object is created
    time_of_creation = models.DateTimeField(auto_now_add=True)
    paused = models.BooleanField(default=False)

class Images(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_images")
    # null=True, blank=True images are not required
    images = models.ImageField(upload_to="images/")
