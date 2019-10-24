from django import forms
from .models import Reservation


Time_CHOICES = [
    ['8', '08:00'],
    ['9', '09:00'],
    ['10', '10:00']
]


class ReservationForm(forms.ModelForm):
    start_date = forms.DateField(
        label='',
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateTimeInput(attrs={
            'placeholder': "Date of Filling",
            'type': "date",
        })
    )
    start_time = forms.ChoiceField(
        label='',
        widget=forms.Select,
        choices=Time_CHOICES,
        initial='8',
        required=True
    )
    price_plan = forms.ChoiceField(
        label='',
        widget=forms.Select,
        # choices=PLAN_CHOICES,
    )
    name = forms.CharField(
        label='',
        max_length=200,
    )
    email = forms.EmailField(
        label='',
        max_length=200,
    )
    child_age = forms.CharField(
        label='',
        max_length=10,
        widget=forms.NumberInput()
    )
    allergy = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )
    vaccination = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )
    illness = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )
    travel_insurance = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )
    wifi = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )
    note = forms.CharField(
        label='',
        max_length=2000,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )

    class Meta:
        model = Reservation
        fields = (
            'start_date', 'start_time', 'price_plan', 'name', 'email', 'child_age', 'allergy', 'vaccination', 'illness',
            'travel_insurance', 'wifi', 'note'
        )
