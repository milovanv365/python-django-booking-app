from django.shortcuts import render, redirect
from .forms import ReservationForm
from service.models import Nursery
from reservation.models import Reservation, Payment
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
import json


# @login_required
def reservation_add(request, nursery_id):
    current_user = request.user

    if current_user.is_authenticated is False:
        return redirect('signin')

    user_type = current_user.groups.get(user=current_user).name

    if user_type == 'Vendor':
        return redirect('service:VendorDashboard')

    nursery = Nursery.objects.get(id=nursery_id)
    nursery_img = nursery.image.url
    nursery_name = nursery.name

    price_plans = json.loads(nursery.price_plan)
    price_plan_choices = [(price_plan['price'], price_plan['time']) for price_plan in price_plans]

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        form.fields['price_plan'].choices = price_plan_choices
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.period = form.data['plan_hour']
            reservation.price = form.cleaned_data['price_plan']
            reservation.nursery = nursery
            reservation.user = current_user
            reservation.save()

            reservation_id = reservation.id
            return redirect('reservation:ReservationConfirm', reservation_id)
    else:
        form = ReservationForm()
        form.fields['price_plan'].choices = price_plan_choices

    context = {
        'form': form,
        'nursery_name': nursery_name,
        'nursery_img': nursery_img
    }
    return render(request, 'reservation_add.html', context)


def reservation_transaction(request, reservation_id):
    current_user = request.user

    if current_user.is_authenticated is False:
        return redirect('signin')

    user_type = current_user.groups.get(user=current_user).name

    if user_type == 'Vendor':
        return redirect('service:VendorDashboard')

    reservation = Reservation.objects.get(id=reservation_id)
    nursery = Nursery.objects.get(id=reservation.nursery_id)
    nursery_img = nursery.image.url
    nursery_name = nursery.name

    stripe.api_key = settings.STRIPE_SECRET_KEY
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    total = reservation.price
    stripe_total = int(total) * 100
    description = 'Travel Sitter - Reserve'

    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingcity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingcity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency="usd",
                description=description,
                customer=customer.id
            )

            payment = Payment.objects.create(
                token=token,
                total=total,
                emailAddress=email,
                billingName=billingName,
                billingAddress1=billingAddress1,
                billingCity=billingcity,
                billingPostcode=billingPostcode,
                billingCountry=billingCountry,
                shippingName=shippingName,
                shippingAddress1=shippingAddress1,
                shippingCity=shippingcity,
                shippingPostcode=shippingPostcode,
                shippingCountry=shippingCountry,
                nursery=nursery,
                user=current_user,
                reservation=reservation
            )

        except stripe.error.CardError as e:
            return False, e
    else:
        pass

    context = {
        'reservation': reservation,
        'nursery_name': nursery_name,
        'nursery_img': nursery_img,
        'data_key': data_key,
        'stripe_total': stripe_total,
        'description': description
    }
    return render(request, 'reservation_transaction.html', context)
