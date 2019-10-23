from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import City


cities = City.objects.all().order_by('id')
CITY_CHOICES = []
for city in cities:
    city_id = city.id
    city_name = city.name
    temp = [city_id, city_name]
    CITY_CHOICES.append(temp)


class SignUpForm(UserCreationForm):
    user_group_item = [
        ('Customer', 'Customer'),
        ('Vendor', 'Child Care Center')
    ]

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, help_text='eg. youremail@anyemail.com')
    user_type = forms.ChoiceField(choices=user_group_item, widget=forms.RadioSelect, initial='Customer')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'user_type')


class NurseryForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=200,
        required=True,
    )

    slug = forms.CharField(
        label='Slug',
        max_length=200,
        required=True,
    )

    description = forms.CharField(
        label='Description',
        max_length=200,
        required=False
    )
    address = forms.CharField(
        label='Address',
        max_length=200,
        required=False,
    )
    telephone = forms.CharField(
        label='Telephone',
        max_length=200,
        required=False,
    )
    station = forms.CharField(
        label='Station',
        max_length=200,
        required=False,
    )
    city = forms.ChoiceField(
        widget=forms.Select,
        choices=CITY_CHOICES,
    )
    time_one = forms.CharField(
        label='',
        max_length=10,
        required=False,
        widget=forms.NumberInput()
    )
    price_one = forms.CharField(
        label='',
        max_length=10,
        required=False,
        widget=forms.NumberInput()
    )
    time_two = forms.CharField(
        label='',
        max_length=10,
        required=False,
        widget=forms.NumberInput()
    )
    price_two = forms.CharField(
        label='',
        max_length=10,
        required=False,
        widget=forms.NumberInput()
    )
    time_three = forms.CharField(
        label='',
        max_length=10,
        required=False,
        widget=forms.NumberInput()
    )
    price_three = forms.CharField(
        label='',
        max_length=10,
        required=False,
        widget=forms.NumberInput()
    )
    image = forms.ImageField(
        required=False
    )
    stock = forms.CharField(
        label='Stock',
        max_length=10,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': ''})
    )