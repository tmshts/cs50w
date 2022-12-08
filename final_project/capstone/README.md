Casa is a simple web application for real estate marketplace/database. On one hand, a person or a company can register and add a property to be sold or rent. On the other hand, an user can just look for a property to rent or buy without registering.


# Distinctiveness and Complexity
Why do I believe that this web application is different than any other projects?

1)	Leaflet map
Leaflet map is a JavaScript library for interactive maps. This library has not been used in any Harvard lecture, hence I needed to get familiar with it in order to be able show coordinates of properties and play around with that map.
2)	Filter & Order
I used class based ListViews in order to easily manipulate with dataset and paginate the dataset. The main reason why I used ListView class is to use filter & order for all the properties/properties for Sales and properties for Rent. Django filter & order are features provided by Django.
3)	Reset password
I am convinced that reset password is necessary for any web application. Therefore, I used this feature provided by django. As I do not have any email provider, I am not able to send an email. But I can get this email/template to be shown in terminal. Consequently, the link has just to be copied into web browser.
4)	API for address
While creating an property, an user can just type a part of an address and some addresses will popup thanks to fetch of URL https://nominatim.openstreetmap.org/search?. Please see more info in create.js.
5)	ImageField
I used ImageField so that an user can upload multiple pictures.
6)	Templatetags
Using mytemplatetags.py in order to go to another page within the filtered dataset from Django. It keeps the filter.
7)	Multiselectfield
I used MultiSelectField in order to list all the possible amenities for property.
8)	django.contrib.humanize
I used django.contrib.humanize so that numbers are easily read by an user.


# What’s contained in each file I created

## File Structure
```
├── capstone
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── casa
│   ├── admin.py
│   ├── apps.py
│   ├── choices.py
│   ├── filters.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── static
│   │   └── casa
│   │       ├── create.js
│   │       ├── index.js
│   │       ├── portfolio.js
│   │       ├── property.js
│   │       └── styles.css
│   ├── templates
│   │   └── casa
│   │       ├── create.html
│   │       ├── error.html
│   │       ├── index.html
│   │       ├── layout.html
│   │       ├── login.html
│   │       ├── pagination.html
│   │       ├── password_reset_complete.html
│   │       ├── password_reset_confirm.html
│   │       ├── password_reset_done.html
│   │       ├── password_reset.html
│   │       ├── portfolio.html
│   │       ├── property.html
│   │       ├── register.html
│   │       ├── rent.html
│   │       ├── reset_password.txt
│   │       └── sales.html
│   ├── templatetags
│   │   └── mytemplatetags.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── media
│   └── images
└── requirements.txt
```

## Capstone
### settings.py
I added some lines into settings.py:
* I added '127.0.0.1', 'localhost' into ALLOWED_HOSTS
* I added ‘casa’, 'multiselectfield', 'django.contrib.humanize' and 'django_filters' into INSTALLED_APPS.
* I added AUTH_USER_MODEL = 'casa.User'
* I added MEDIA_ROOT = os.path.join(BASE_DIR, 'media') and MEDIA_URL = '/media/' in order to be able to store images.
- I added EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' in order to be able see a template for reset password in terminal.

### urls.py
I needed to import from django.contrib.auth import views as auth_views in oder to be able reset password.

## Casa
### static\casa
#### create.js
This JavaScript file is responsible for a couple of things:
1)	finding an address thanks to search API provided from Nominatim. Nominatim is tool how to search OpenStreetMap data by an address. For this purpose, I used fetch.
2)	The result, which are the addresses, is shown in create.html. An user can click on each address.
3)	By clicking on an address, another function is called. There are 3 arguments in this function, such as address, latitude and longitude. These arguments are then filled into the corresponding fields in the create.html. Now, the leaflet map comes into play. Leaflet is an open-source JavaScript library for interactive maps. This library is free compared to Google Map and hence I use it. First, I initialize a map and set the coordinates. Next, I add Layer from OpenStreetMap which is basically the graphical part of map. Then, I create a marker with the coordinates representing the selected address by an user.

#### index.js
This JavaScript file relates to index.html, rent.html and sales.html. The only difference between index.html, rent.html and sales.html is that index.html contains properties for sales and rent. The structure of these files is identical though.

If an user wants to change the currency, he/she just selects either USD, MXN or EUR. Consequently, fetching a free foreign exchange rate API is triggered which calculates a current exchange rate for wished currency. Then, all the prices in all the divs at only current page are changed correspondingly. On the other hand, if an user changes the metric for size, there is no need to fetch but just static formula is used. Thus, all the sizes in all the divs are changed but only at current page.

Moreover, if a filter button is clicked, the form related to filter appears. This form can also disappear when user clicks on cancel.

According to the https://worship.agency/mobile-screen-sizes-for-2021, the widest screen of a smartphone has about 414 px. For this reason, if width of screen (document.documentElement.clientWidth) is less than 450 pixels, the structure of listings and a map of index.html, sales.html and rent.html will change in order to be mobile-responsive. All other html files are mobile-responsive without using document.documentElement.clientWidth.

The other important part of the index.js is leaflet map. By loading page, a map is initialized, the coordinates of map are set for the United States and the Layer is from Open Street Map. The point is to put all the properties/divs on a current page into the leaflet map. For this reason, I select all the visible divs on the current page and extract (innertHTML) some important values from the properties such as latitude, longitude, address and others. Thanks to the latitude and longitude of each property, I can create marker for every property. Each marker has an individual label with price. In addition to this, I also use popup window for each marker. There are all the necessary information about property in the popup window. When an user clicks on a pop up window, he/she is redirected to property page. 

#### portfolio.js
In terms of currency and size metric, it works the same like in index.js.

Moreover, there are 2 buttons on each property/div. Delete button and pause button. By clicking on delete button, the property is completely deleted from database. For this purpose, I use fetch which communicates with back-end. Also the div is removed from front-end. By clicking on pause button, the property is just paused or activate from listings. I made a decision to use CSRF token instead of adding @csrf_exempt in to the views.py. I took the CSRF token function from https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax. Then, I put the CSRF token into headers in fetch. This CSRF token may be useful in the feature, once the features of this web app grow and hence this project becomes bigger.

An user is also able to click on All, Sales or Rent buttons. After clicking on All, all the properties are shown. When clicking on Sales, the properties for Sales are shown and the properties for Rent are hidden. The same principle is for Rent button. This process is based on visibility of the divs.

Last feature of portfolio.js is how to order properties/divs based on date, size or price. An user can add many properties and so he/she would like to order his/her properties based on some criterium in order to have a nice overview. For this reason, it is necessary to get all the divs and then extract important values such as date, size or price. In order to compare 2 values, I used a sort function. When it comes to date, I had to extract date/timestamp. The point is that Django saves the timestamp in a certain format. Therefore, I needed to split, replace and then concatenate the strings in order to get date in wished format string. Then, I needed to create an object of class Date. Hence, I created a new Date based on this final date in string. As a result, I was able to compare 2 different Dates. In terms of size and price, the comparison was easier as I just extracted values (innerHTML) from portfolio.html and these values could be immediately compared thanks to sort function. Finally, the ordered values could be then placed on the current page.

#### property.js
An user can edit description, price and title thanks to fetch which communicates with back-end. Thus, the fields are updated without refreshing the page.

An user can delete all the pictures thanks to fetch. But at this time, the page has to be refreshed so that the request.method is GET and thus the ImageForm is shown. Once the ImageForm is shown, an user can upload the pictures.

Another fetch is used when it comes to showing contact details. If someone is interested in a certain property, this person can click on Show Contact and corresponding contact details are shown.

By loading property.html page, a map is initialized and the coordinates of a property are set. The Layer from Open Street Map is again used. Furthermore, a marker with title of a property is also added to the map.

#### styles.css
This file describes how HTML elements should be displayed.

### templates/casa
#### create.html
create.html contains PropertyForm and ImageForm. While creating a property, an user can also select option from PropertyType and SalesRent. PropertyForm represents basically the Property model. ImageForm represents Images model. PropertyType and SalesRent are models. The possible options from PropertyType and SalesRent are added by admin.
create.html also contains script create.js and script for leaflet map.

#### error.html
In case of certain errors in views.py, the error.html with the error message is rendered.

#### index.html
Index.html contains all the listings, currency and metric for size options. The important part of index.html is filter for properties and properties. Each property is in div showing important features such as main picture, price, size, address of a property, etc. Another crucial aspect of index.html is div for map. Index.html includes pagination.html. Scripts for Index.js and leaflet map are added to index.html.

#### layout.html
Layout.html contains links for bootstrap, styles.css and leaflet map. Navigation bar and footer are added to layout.html as all the pages will have the same navigation bar and footer.

#### login.html
Login.html contains a form for login credentials of users. An user can also reset his/her password by clicking on “Forgotten your password?”.  If a person is not registered, she/he can do so by clicking on “Not a member?”.

#### pagination.html
An user can click on next/previous page thanks to the pagination.html. This html file loads important mytemplatetags file.

#### password_reset_complete.html
Template for password reset complete.

#### password_reset_confirm.html
Template for password reset confirmation.

#### password_reset_done.html
Template for password reset sent.

#### password_reset.html
Template for entering an email address of an user. The PasswordResetForm provided by Django is used. Then, an user should receive an email with all the instructions. As this web application does not have any email provider, the instructions will be printed in terminal. In the real world, it is necessary to have an email provider which sends the instructions to the user´s email.

#### portfolio.html
Portfolio.html contains order, currency and metric for size options. Furthermore, the buttons for all the listings, rent listings and sales listings are included. The important part of portfolio.html are properties. Each property is in div showing important features such as main picture, price, size, address of a property, etc. Also, buttons for delete or pause/activate property are in each div. Script for portfolio.js is added to portfolio.html.

#### property.html
Property.html contains all the information about property including pictures. If current user is equal to the user who created this property, the buttons for edit title, price and description are shown. Moreover, div for leaflet map and the button for showing contact details are also added. Scripts for property.js and leaflet map are added to property.html.

#### register.html
Register.html contains important input fields so that a person or company can register.

#### rent.html
This template is almost identical like index.html but only properties for rent are listed.

#### reset_password.txt
This txt file contains a message which will be sent to the user´s email in the real world. For a purpose of this final project, this message will be printed in terminal and the URL link will be copied and then paste into web browser.

#### sales.html
This template is almost identical like index.html but only properties for sales are listed.

### templatetags
#### mytemplatetags.py
This file is an important file which is responsible for keeping filter while going to next/previous page. If there was not this file and an user clicked on next page in index.html, the filter would be reset automatically. In other words, filter can work properly through all the pages of properties.

### admin.py
File admin.py contains all the models so that these models can be seen in Django administration.

### choices.py
There are choices for amenities, number of bedrooms, number of bathrooms and ordering choices for filter in this file. The choices for amenities, number of bedrooms and number of bathrooms can be changed. These changes then will be reflected while adding a new property. Even Ordering choices can be changed, but then filters.py must be also changed accordingly.

### filters.py
This file contains django_filters.FilterSet. This FilterSet generates filter for model Property. In fact, this filter is based on the fields of the model Property. An important part of this customizable filter is also an option to order the listings based on some criterium such as price, timestamp and size.

### models.py
models.py contains 5 models: User, SalesRent, PropertyType, Property and Images

### urls.py
There are different URL paths for this web application in this file. I also added urlpatterns for media so that the uploaded pictures are stored in media folder.

### views.py 
This file is a back-end logic and it is a bridge between django database and front-end.

This file constains:
* Form related to Property model
* Form related to Images model
* Class based ListViews for index, sales and rent as it is then easy to use pagination and django filter including orderingfilter
* Function based views for password reset, portfolio, property, creating property, login, logout and register

## Media/images
These folders are created for storing images. User will upload pictures for a property. These pictures will be stored in images folder.

## requirements.txt
This file contains requirements which have to be installed in order to be able to run this web application.



# How to run application

Run in terminal these commands one by one:

First, run following command to install all the necessary dependencies.

```sh
pip install -r requirements.txt
```

Run following 2 commands to make migrations and migrate django database.


```sh
python manage.py makemigrations
```

```sh
python manage.py migrate
```

Synchronize the database:

```sh
python manage.py migrate --run-syncdb
```

Create your super user credentials by running command below:
```sh
python manage.py createsuperuser
```

Run the web application:

```sh
python manage.py runserver
```


After that, open django administration. You have to add Sales and Rent into SalesRent model as it is a real estate web application. If you do not add Sales and Rent, the application will crash because views.py, layout.html and urls.py depend on the words Sales and Rent.

Moreover, you have to add some property types into PropertyType model. Please bear in mind that an user has to select property type while creating a property. For this reason, you may want to add Condo, House and Villa. These property types will be then displayed in django filter as CheckboxSelectMultiple.

Next, very important steps are:
* please uncomment path for sales and rent in urls.py in folder casa.
![image](https://user-images.githubusercontent.com/74012536/204613328-f51b5845-a2d6-4a43-9eaf-ae89dbd89522.png)

* uncomment def sales(request):, class PropertyListViewSales(ListView):, def rent(request):, class PropertyListViewRent(ListView): in views.py.
![image](https://user-images.githubusercontent.com/74012536/204613476-a7be8a99-6d40-4a01-9b5d-54c8974943d0.png)
![image](https://user-images.githubusercontent.com/74012536/204613576-18a340aa-b21b-4368-b40b-d0988f1fa44c.png)

* delete {% comment "Optional note" %} {% endcomment %} in layout.html.
![image](https://user-images.githubusercontent.com/74012536/204613641-ea74f2d8-dbe7-487d-af37-facf73885ac4.png)


Now, you are able to fully use the web application Casa.

# Any other additional information the staff should know about my project
My plan is to launch this simple web application on the Mexican market. I am aware of the fact that very important feature is still missing such as ‘search properties in that area’ button in the leaflet map. I still hope that this web application satisfies your requirements.

I would be more than happy to get a feedback in order to improve my web app. 
