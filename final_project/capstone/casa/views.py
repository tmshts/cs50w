import re
from turtle import width
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Property, PropertyType, SalesRent, Images, User
from .filters import PropertyFilter#, PropertyOrder

from django.contrib.auth.decorators import login_required
from django import forms
from casa.choices import *
#from multiselectfield import MultiSelectField
#from django_countries.fields import CountryField
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# added
import json
import requests
from django.db.models import F
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.contrib.auth import get_user_model
User = get_user_model()
#from django.contrib import messages

from django.views.generic.list import ListView


class PropertyForm(forms.Form):
    amenities = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=AMENITIES_CHOICES, required=False)
    total_bedroom = forms.ChoiceField(choices=TOTAL_BEDROOM_CHOICES)
    total_bathroom = forms.ChoiceField(choices=TOTAL_BATHROOM_CHOICES)
    size = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'ft²', 'class': 'inputfield_number'}))
    title = forms.CharField(label="",
                            max_length=200,
                            widget= forms.TextInput(attrs={'placeholder': 'Title Of Your Property', 'class': 'inputfield_text'}))
    
    # 'readonly':'readonly'
    address = forms.CharField(max_length=2000,
                                    widget= forms.TextInput(attrs={'class': 'address_inputfield'}))
    longitude = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'inputfield_number'}))
    latitude = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'inputfield_number'}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Write Description of Your Property', 'class': 'inputfield_text', 'style': 'width: 100%'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Price', 'class': 'inputfield_number'}))
    image_url = forms.URLField(max_length=2000, required=False)

class ImageForm(forms.Form):
    # required=False
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": True}))

def index(request):

    if request.method == 'GET':
        property_filter = PropertyFilter(request.GET, queryset=Property.objects.filter(paused=False))
        form = property_filter.form

        context = {
            "properties": property_filter.qs,
            "form": form,
        }

        return render(request, "casa/index.html", context)


# Class based view index
class PropertyListView(ListView):
    paginate_by = 15
    queryset = Property.objects.filter(paused=False).order_by("-time_of_creation")
    template_name = 'casa/index.html'
    context_object_name = 'properties'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PropertyFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

"""
def sales(request):
    property_filter = PropertyFilter(request.GET, queryset=Property.objects.filter(paused=False))

    form = property_filter.form
    context = {
        "properties": property_filter.qs,
        "form": form
    }
    return render(request, "casa/sales.html", context)

# Class based view sales
class PropertyListViewSales(ListView):
    paginate_by = 15
    sales_rent = SalesRent.objects.get(sales_or_rent='Sales')
    queryset = Property.objects.filter(sales_rent=sales_rent, paused=False).order_by("-time_of_creation")
    template_name = 'casa/sales.html'
    context_object_name = 'properties'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PropertyFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

def rent(request):
    #sales_rent = SalesRent.objects.get(sales_or_rent='Rent')
    property_filter = PropertyFilter(request.GET, queryset=Property.objects.filter(paused=False))
  
    form = property_filter.form
    context = {
        "properties": property_filter.qs,
        "form": form
    }
    return render(request, "casa/rent.html", context)

# Class based view rent
class PropertyListViewRent(ListView):
    paginate_by = 15
    sales_rent = SalesRent.objects.get(sales_or_rent='Rent')
    queryset = Property.objects.filter(sales_rent=sales_rent, paused=False).order_by("-time_of_creation")
    template_name = 'casa/rent.html'
    context_object_name = 'properties'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PropertyFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context
"""

def password_reset(request):

    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            print(email)
            user = User.objects.filter(email=email)
            #associated_users = User.objects.filter(Q(email=data))
            if user.exists():
                for user in user:
                    subject = "Password Reset Requested"
                    email_template = "casa/reset_password.txt"
                    message = {
                    "username": user.username,
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Casa',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template, message)
                    try:                          # admin email should be changed accordingly
                        send_mail(subject, email, 'tmshts@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    #messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return render(request, "casa/password_reset_done.html")
                    #return HttpResponseRedirect(reverse("password_reset_done"))
                
            else:
                error = 'There is no user with this email in our database.'
                return render(request, "casa/error.html", {
                    'error': error,
                })
    else:
        password_reset_form = PasswordResetForm()
        return render(request, "casa/password_reset.html", {
            "password_reset_form":password_reset_form,
            }) 


#@login_required
def portfolio(request):
    if request.user.is_authenticated:
        properties = Property.objects.filter(listed_by_user=request.user.id).order_by("-time_of_creation")
        properties_id = properties.values_list('pk', flat=True)
        # List for values with Pause Property or Activate Property
        current_values = []

        for value in properties_id:
            value_string = property_activate_handler(value)
            current_values.append(value_string)

        zipped_list = zip(properties, current_values)

        return render(request, "casa/portfolio.html", {
            'properties': properties,
            'context': zipped_list
        })
    else:
        error = 'You have to log in and add a property in order to see your portfolio.'
        return render(request, "casa/error.html", {
            'error': error,
        })

def property_activate_handler(property_id):
    # Check follow or not follow button
    activate_value = ''
    property_instance = Property.objects.get(id=property_id)
    property_value = property_instance.paused
    if property_value == True:
        activate_value = "Activate Property"
    else:
        activate_value = "Pause Property"

    return activate_value

def property(request, property_id):

    current_user = request.user
    # Query for requested property
    try:
        property = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        error = 'Your searched property does not exist.'
        return render(request, "casa/error.html", {
            'error': error,
        })
        #return JsonResponse({"error": "Property not found."}, status=404)

    if request.method == "POST":

        if 'new_pictures' in request.POST: # in property.html
            #imageform = ImageForm(request.POST)
            files = request.FILES.getlist("images")

            if len(files) > 30:
                imageform = ImageForm()
                error = "You can upload maximum 30 images."

                return render(request, "casa/property.html", {
                    'property': property,
                    'current_user': current_user,
                    'imageform': imageform,
                    'error': error
                })

            #if imageform.is_valid():
            property_instance = Property.objects.get(id=property_id)
            for i in files:
                Images.objects.create(property=property_instance, images=i)
            return HttpResponseRedirect(reverse("property", args=(property_id,)))

        else:
            data = json.loads(request.body)
            # Delete Property
            if "prop_id" in data:
                property_id = data["prop_id"]
                Property.objects.filter(id=property_id).delete()

                return JsonResponse({})

            # Delete Pictures
            if "property_id" in data:
                property_id = data["property_id"]
                property_instance = Property.objects.get(id=property_id)
                print(property)
                Images.objects.filter(property=property_instance).delete()

                return JsonResponse({})
                
            # Show Contacts
            if "pro_id" in data:
                property_id = data["pro_id"]
                property_instance = Property.objects.get(id=property_id)

                whatsapp = property_instance.listed_by_user.phonenumber
                email = property_instance.listed_by_user.email

                return JsonResponse({"whatsapp": whatsapp, "email": email})
                

            # Pause or Active Property
            if "active_pause_property_id" in data:
                property_id = data["active_pause_property_id"]
                property_instance = Property.objects.get(id=property_id)
                post_value = ''
                actual_value = property_activate_handler(property_instance.id)

                if actual_value == 'Activate Property':
                    property_instance.paused = False
                    property_instance.save()
                    post_value = 'Pause Property'
                #if actual_value == 'Pause Property':
                else:
                    property_instance.paused = True
                    property_instance.save()
                    post_value = 'Activate Property'

                return JsonResponse({"value": post_value})

            if "edited_text" in data:
                edited_text = data["edited_text"]
                # Update post
                Property.objects.filter(pk=property_id).update(description_of_property=edited_text)
                # Get updated post
                description = Property.objects.get(pk=property_id).description_of_property
                return JsonResponse({"description": description})

            if "edited_price" in data:
                edited_price = data["edited_price"]
                # Update post
                Property.objects.filter(pk=property_id).update(price=edited_price)
                # Get updated post
                price = Property.objects.get(pk=property_id).price
                return JsonResponse({"price": price})

            if "edited_title" in data:
                edited_title = data["edited_title"]
                # Update post
                Property.objects.filter(pk=property_id).update(title_of_property=edited_title)
                # Get updated post
                title = Property.objects.get(pk=property_id).title_of_property
                return JsonResponse({"title": title})

    if request.method == "GET":    
        # property = Property.objects.get(pk=property_id)
        property_user = property.listed_by_user.username

        #imageform = ImageForm()
        images_instance = Images.objects.filter(property=property)

        imageform = ImageForm()

        if (property.paused == False):

            if len(images_instance) == 0:

                return render(request, "casa/property.html", {
                    'property': property,
                    'current_user': current_user,
                    'imageform': imageform,
                })
            else:
                return render(request, "casa/property.html", {
                        'property': property,
                        'images': images_instance,
                        'current_user': current_user,

                    })
        elif (property.paused == True and str(property_user) == str(current_user)):

            if len(images_instance) == 0:
                imageform = ImageForm()

                return render(request, "casa/property.html", {
                    'property': property,
                    'current_user': current_user,
                    'imageform': imageform,

                })
            else:
                return render(request, "casa/property.html", {
                        'property': property,
                        'images': images_instance,
                        'current_user': current_user,

                    })   
        else:
            error = 'Your searched property does not exist.'
            return render(request, "casa/error.html", {
                'error': error,
            })

#@login_required
def create(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            # I get PK of one category and this object is saved in variable category
            form = PropertyForm(request.POST)
            files = request.FILES.getlist("images")
            #images =request.FILES.get('images')

            if len(files) > 30:
                form = PropertyForm()
                imageform = ImageForm()
                error = "You can upload maximum 30 images."

                return render(request, "casa/create.html", {
                    "PropertyType": PropertyType.objects.all(),
                    "SalesRent": SalesRent.objects.all(),
                    'form': form,
                    'imageform': imageform,
                    'error': error
                })
            
            if form.is_valid():
                total_bedroom = int(form.cleaned_data["total_bedroom"])
                total_bathroom = float(form.cleaned_data["total_bathroom"])
                size = form.cleaned_data["size"]

                amenities = form.cleaned_data["amenities"]
                title = request.POST.get('title')

                # Get input_address + coordinates
                address = form.cleaned_data["address"]
                longitude = form.cleaned_data["longitude"]
                longitude = longitude
                latitude = form.cleaned_data["latitude"]
                latitude = latitude

                # Fetch coordinates to get address in order to fill it in model
                # NOT WORKING WITH LATITUDE AND LONGITUDE
                lat = latitude
                lon = longitude
                #base_url = 'https://nominatim.openstreetmap.org/reverse'
                #request_url = f"{base_url}?lat={lat}&lon={lon}&format=geocodejson"
                #response = requests.get(request_url)

                base_url = 'https://nominatim.openstreetmap.org/search'
                params = {
                    'q': address,
                    'format': 'json',
                    'addressdetails': 1,
                    'limit': 1,
                    'polygon_svg': 1,
                }
                response = requests.get(url=base_url, params=params)
                #print(response)
                if response.status_code == 200:
                    # returns JSON object as dictionary
                    response = response.json()
                    print(response)
                    #print(type(response))
                    try:
                        # Get address features from list

                        # Street
                        street_name = 'name'
                        if 'street' in response[0]['address']:
                            street_name = response[0]['address']['street']
                            street_name = street_name.replace('"','')
                        elif 'road' in response[0]['address']:
                            street_name = response[0]['address']['road']
                            street_name = street_name.replace('"','')

                        street_name = str(street_name.capitalize())
                        print(street_name)

                        # Street number
                        street_number = 0
                        if 'house_number' in response[0]['address']:
                            street_number = response[0]['address']['house_number']
                            street_number = street_number.replace('"','')
                        else:
                            street_number = 0

                        street_number = int(street_number)
                        print(street_number)

                        # City
                        city = 'name'
                        if 'town' in response[0]['address']:
                            city = response[0]['address']['town']
                            city = city.replace('"','')
                        elif 'city' in response[0]['address']:
                            city = response[0]['address']['city']
                            city = city.replace('"','')
                                                
                        city = str(city.capitalize())
                        print(city)

                        # State
                        state = 'name'
                        if 'state' in response[0]['address']:
                            state = response[0]['address']['state']
                            state = state.replace('"','')
                        elif 'neighbourhood' in response[0]['address']:
                            neighbourhood = response[0]['address']['neighbourhood']
                            state = neighbourhood.replace('"','')

                        state = str(state.capitalize())
                        print(state)

                        # Postal Code
                        postal_code = response[0]['address']['postcode']
                        postal_code = postal_code.replace('"','')
                        postal_code = int(postal_code)
                        print(postal_code)

                        # Country
                        country = response[0]['address']['country']
                        country = country.replace('"','')
                        country = str(country)
                        print(country)
                        if country != 'United States':
                            form = PropertyForm()
                            imageform = ImageForm()
                            error = "You can only create a property which is located in the United States"

                            return render(request, "casa/create.html", {
                                "PropertyType": PropertyType.objects.all(),
                                "SalesRent": SalesRent.objects.all(),
                                'form': form,
                                'imageform': imageform,
                                'error': error
                            })                            

                    # any exception
                    except:
                        form = PropertyForm()
                        imageform = ImageForm()
                        error = "There may be something wrong with your address, longitude or/and latitude. Please try it again in a while."

                        return render(request, "casa/create.html", {
                            "PropertyType": PropertyType.objects.all(),
                            "SalesRent": SalesRent.objects.all(),
                            'form': form,
                            'imageform': imageform,
                            'error': error
                        })
                # no 200 status code
                else:
                    form = PropertyForm()
                    imageform = ImageForm()
                    error = "There is a lot of requests. Please try it again."

                    return render(request, "casa/create.html", {
                        "PropertyType": PropertyType.objects.all(),
                        "SalesRent": SalesRent.objects.all(),
                        'form': form,
                        'imageform': imageform,
                        'error': error
                    })

                # Can be easily modified
                country = 'United States of America'
            
                description = form.cleaned_data["description"]
                price = form.cleaned_data["price"]
                # I get username tmshts
                username_instance = User.objects.get(pk=request.user.id)

                property_type = request.POST.get('property_type')
                property_type_instance = PropertyType.objects.get(pk=int(property_type))

                sales_or_rent = request.POST.get('sales_or_rent')
                sales_or_rent_instance = SalesRent.objects.get(pk=int(sales_or_rent))
            
                property_obj = Property.objects.create(amenities=amenities, bedroom=total_bedroom, bathroom=total_bathroom, size=size, title_of_property=title, sales_rent=sales_or_rent_instance, description_of_property=description, price=price, type_of_property=property_type_instance, listed_by_user=username_instance, street_name=street_name, street_number=street_number, city=city, state=state, country=country, postal_code=postal_code, longitude=longitude, latitude=latitude)
                property_obj.save()

                for i in files:
                    Images.objects.create(property=property_obj, images=i)
                #messages.success(request, "New Property Added")
                return HttpResponseRedirect(reverse("portfolio"))
        
        else: # GET
            form = PropertyForm()
            imageform = ImageForm()

            return render(request, "casa/create.html", {
                "PropertyType": PropertyType.objects.all(),
                "SalesRent": SalesRent.objects.all(),
                'form': form,
                'imageform': imageform
            })
    else:
        error = 'You have to log in to create a property.'
        return render(request, "casa/error.html", {
            'error': error,
        })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "casa/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "casa/login.html")
        

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        company_name = request.POST["company_name"]
        representative = request.POST["representative"]

        phonenumber = request.POST["phonenumber"]
        phonenumber.strip()
        phonenumber = (f'{phonenumber[:3]}-{phonenumber[3:6]}-{phonenumber[6:]}')

        # User must register as Person or Company
        if (not first_name and not last_name) and (not company_name and not representative):
            return render(request, "casa/register.html", {
                "message": "You must register as Person or Company."
            })

        # Person with full name
        elif (first_name and not last_name and not company_name and not representative) or (not first_name and last_name and not company_name and not representative):
            return render(request, "casa/register.html", {
                "message": "Person must register with the full name."
            })

        # Company with Representative name
        elif (not first_name and not last_name and not company_name and representative) or (not first_name and not last_name and company_name and not representative):
            return render(request, "casa/register.html", {
                "message": "Company must register with Company Name and Representative Name."
            })

        # User can register either as Person or Company
        elif (first_name or last_name) and (company_name or representative):
            return render(request, "casa/register.html", {
                "message": "Register as Person (including First and Last Name) or Company (Company Name and Representative Name)."
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "casa/register.html", {
                "message": "Passwords must match."
            })

        # Same email check
        user = User.objects.filter(email=email)
        if user.exists():
            return render(request, "casa/register.html", {
                "message": "Email is already taken."
            })        

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.company_name = company_name
            user.representative = representative
            user.phonenumber = phonenumber
            user.save()
        except IntegrityError:
            return render(request, "casa/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "casa/register.html")
