import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import City, NurseryLimit
from ericashop.helper import Helper


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
        label='',
        max_length=200,
        required=True,
    )

    slug = forms.CharField(
        label='',
        max_length=200,
        required=True,
    )

    description = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )
    address = forms.CharField(
        label='',
        max_length=200,
        required=False,
    )
    telephone = forms.CharField(
        label='',
        max_length=200,
        required=False,
    )
    station = forms.CharField(
        label='',
        max_length=200,
        required=False,
    )
    city = forms.ChoiceField(
        label='',
        widget=forms.Select,
        choices=CITY_CHOICES,
    )
    time_one = forms.CharField(
        label='',
        max_length=10,
        widget=forms.NumberInput()
    )
    price_one = forms.CharField(
        label='',
        max_length=10,
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
        label='',
        max_length=10,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': ''})
    )


class NurseryLimitForm(forms.ModelForm):
    date = forms.DateField(
        label='',
        required=True,
        initial=datetime.date.today(),
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            attrs={
                'type': "date",
                "class": "js-start-date"
            },
        )
    )
    time_from = forms.ChoiceField(
        label='',
        widget=forms.Select,
        choices=Helper.Time_CHOICES,
        initial='9',
        required=True
    )
    time_to = forms.ChoiceField(
        label='',
        widget=forms.Select,
        choices=Helper.Time_CHOICES,
        initial='23',
        required=True
    )

    class Meta:
        model = NurseryLimit
        fields = (
            'date', 'time_from', 'time_to'
        )

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date
