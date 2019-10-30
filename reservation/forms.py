from django import forms
from .models import Reservation
import datetime


Time_CHOICES = [
    ['0', '00:00'],
    ['1', '01:00'],
    ['2', '02:00'],
    ['3', '03:00'],
    ['4', '04:00'],
    ['5', '05:00'],
    ['6', '06:00'],
    ['7', '07:00'],
    ['8', '08:00'],
    ['9', '09:00'],
    ['10', '10:00'],
    ['11', '11:00'],
    ['12', '12:00'],
    ['13', '13:00'],
    ['14', '14:00'],
    ['15', '15:00'],
    ['16', '16:00'],
    ['17', '17:00'],
    ['18', '18:00'],
    ['19', '19:00'],
    ['20', '20:00'],
    ['21', '21:00'],
    ['22', '22:00'],
    ['23', '23:00']
]


class ReservationForm(forms.ModelForm):
    start_date = forms.DateField(
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
    start_time = forms.ChoiceField(
        label='',
        widget=forms.Select,
        choices=Time_CHOICES,
        initial='9',
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
    child_number = forms.CharField(
        label='',
        max_length=10,
        initial='1',
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
            'start_date', 'start_time', 'price_plan', 'name', 'email', 'child_age', 'child_number', 'allergy',
            'vaccination', 'illness', 'travel_insurance', 'wifi', 'note'
        )

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return start_date
