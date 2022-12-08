import django_filters
from .models import PropertyType, Property
from django import forms
from django.forms.widgets import TextInput

from django_filters.widgets import RangeWidget

from casa.choices import *

#class PropertyOrder(django_filters.FilterSet):
#    name = django_filters.CharFilter(lookup_expr='icontains')

#    CHOICES = (
#        ('price', 'Price: Low to High'),
#        ('-price', 'Price: High to Low')
#    )

#    order = django_filters.ChoiceFilter(
#        choices=CHOICES,
#        method='ordering_filter',
#        widget=forms.Select(attrs={'class':'filter','id':'ordering'}))



# Custome Range Widget for placeholders
class MyRangeWidget(RangeWidget):

    def __init__(self, min=None, max=None, attrs=None):
        super(MyRangeWidget, self).__init__(attrs)
        if min:
            self.widgets[0].attrs.update(min)
        if max:
            self.widgets[1].attrs.update(max)
        

# Property Filter
class PropertyFilter(django_filters.FilterSet):

    def get_types():
        property_types = ()
        types = PropertyType.objects.filter()
        for type in types:
            property_types += (type.id, type.type_of_property),
        return property_types


    type_of_property = django_filters.MultipleChoiceFilter(choices=get_types,
                                                            label=('Type of Property'),
                                                            widget=forms.CheckboxSelectMultiple(attrs={'empty_label': 'None', 'class': 'checkbox_filter'}),
                                                            )
    street_name = django_filters.CharFilter(lookup_expr='icontains', label=('Street'), widget=TextInput(attrs={'class': 'inputfield_text'}))
    city = django_filters.CharFilter(lookup_expr='iexact', label=('City'), widget=TextInput(attrs={'class': 'inputfield_text'}))
    state = django_filters.CharFilter(lookup_expr='iexact', label=('State'), widget=TextInput(attrs={'class': 'inputfield_text'}))


    price = django_filters.RangeFilter(label='Price in USD', widget=MyRangeWidget(min={'placeholder':'Min'},
                                                            max={'placeholder':'Max'},
                                                            attrs={'class': 'inputfield_number'}))
    size = django_filters.RangeFilter(label='Size in ft²', widget=MyRangeWidget(min={'placeholder':'Min'},
                                                            max={'placeholder':'Max'},
                                                            attrs={'class': 'inputfield_number'}))
    bedroom = django_filters.RangeFilter(widget=MyRangeWidget(min={'placeholder':'Min'},
                                                            max={'placeholder':'Max'},
                                                            attrs={'class': 'inputfield_number'}))
    bathroom = django_filters.RangeFilter(widget=MyRangeWidget(min={'placeholder':'Min'},
                                                            max={'placeholder':'Max'},
                                                            attrs={'class': 'inputfield_number'}))

    order = django_filters.OrderingFilter(
        choices=ORDERING_CHOICES,
        fields = (
            'price', 'price', 'time_of_creation', 'time_of_creation', 'size', 'size'
        ),
        empty_label = None,
        null_label = None,
    )

    #class Meta:
    #    model = Property
        #fields = {
        #    'city': ['iexact'],
        #    'state': ['iexact'],
        #}