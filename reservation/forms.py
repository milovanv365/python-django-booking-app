import datetime
from django import forms
from .models import Reservation
from ericashop.helper import Helper


class ReservationForm(forms.ModelForm):
    start_date = forms.DateField(
        label='',
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
        widget=forms.Select(attrs={"class": "js-start-time"}),
        choices=Helper.Time_CHOICES,
        initial='8'
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
    child_number = forms.CharField(
        label='',
        max_length=1,
        initial='1',
        widget=forms.NumberInput(attrs={"min": 1, "max": 99})
    )
    child_age = forms.CharField(
        label='',
        max_length=1,
        initial=0,
        required=False,
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
            'start_date', 'start_time', 'price_plan', 'price_total', 'name', 'email', 'child_number', 'child_age',  'allergy',
            'vaccination', 'illness', 'travel_insurance', 'wifi', 'note'
        )

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return start_date

    # def clean_price_plan(self):
    #     price_plan = self.cleaned_data['price_plan']
    #     return price_plan

    # def clean_start_time(self):
    #     start_time = self.cleaned_data['start_time']
    #     if start_time == '':
    #         raise forms.ValidationError("Nursery is unavailable on this day!")
    #     return start_time

