from django import forms

TIME_CHOICES = (
        ('10:00-17:00', '10:00-17:00'),
        ('9:00-13:00', '9:00-13:00'), 
        ('13:00-17:00', '13:00-17:00'),
        ('17:00-21:00', '17:00-21:00'),
    )


class ReservationInfoForm(forms.Form):
    rtime = forms.ChoiceField(
        label='Time',
        widget=forms.Select,
        choices=TIME_CHOICES,
        required =True,
    )
    
    your_name = forms.CharField(
        label='Your name',
        max_length =200,
        required =True,                    
    )
    email = forms.EmailField(
         label='Your Email',
         max_length = 200,
         required = True        
    )
    reservation_date = forms.DateTimeField(
         label='Date',
         required=True,
         widget=forms.DateInput(attrs={"type":"date"}),
         input_formats=['%Y-%m-%d']
    )
    age_ofthechild = forms.CharField(
        label='Age of your child',
        max_length=200,
        required=True
    )
    allergies = forms.CharField(
        label='If have an allergy, fill in',
        max_length=2000,
        required=False,
        widget=forms.TextInput()
    )
    vaccinations = forms.CharField(
        label ='If have not recieved a vaccination, fill in',
        max_length=2000,
        required=False,
    )
    illness = forms.CharField(
        label ='If do not want a hospitai in an emergency, fill in',
        max_length=1000,
        required=False,
    )
    travel_insurance = forms.CharField(
        label ='If do not have travel insurance, fill in',
        max_length=1000,
        required=False,
    )
    wifi = forms.CharField(
        label ='If smart phone is not available while traveling, fill in',
        max_length=1000,
        required=False,
    )
    note = forms.CharField(
        label ='A postscript about your child. And, if you have an SNS that can contact, fill in',       
        max_length=2000,
        required=False,  
        widget=forms.TextInput()
    )
