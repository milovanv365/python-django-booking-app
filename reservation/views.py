import json

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from reservation.models import Reservation, Payment
from service.models import Nursery
from .forms import ReservationForm


def reservation_add(request, nursery_id):
    current_user = request.user
    reservation_exist = False

    if current_user.is_authenticated is False:
        return redirect('signin')

    user_type = current_user.groups.get(user=current_user).name

    if user_type == 'Vendor':
        return redirect('service:VendorDashboard')

    nursery = Nursery.objects.get(id=nursery_id)

    price_plans = json.loads(nursery.price_plan)
    price_plan_choices = [(price_plan['price'], price_plan['time']) for price_plan in price_plans]

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        form.fields['price_plan'].choices = price_plan_choices
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_time']
            price = form.cleaned_data['price_plan']

            reservation_check = Reservation.objects.filter(
                user=current_user, nursery=nursery, start_date=start_date, start_time=start_time, price=price
            )

            if len(reservation_check) > 0:
                reservation_exist = True
            else:
                reservation = form.save(commit=False)
                reservation.period = form.data['period']
                reservation.price = form.data['total_price']
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
        'nursery': nursery,
        'reservation_exist': reservation_exist,
    }
    return render(request, 'reservation/add.html', context)


def reservation_transaction(request, reservation_id):
    current_user = request.user
    payment_exist = False

    if current_user.is_authenticated is False:
        return redirect('signin')

    user_type = current_user.groups.get(user=current_user).name

    if user_type == 'Vendor':
        return redirect('service:VendorDashboard')

    reservation = Reservation.objects.get(id=reservation_id)
    if reservation.paymentStatus == 'Payed':
        payment_exist = True
    nursery = Nursery.objects.get(id=reservation.nursery_id)
    nursery_img = nursery.image.url
    nursery_name = nursery.name

    stripe.api_key = settings.STRIPE_SECRET_KEY
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    reservation_price = reservation.price
    stripe_total = int(reservation_price) * 100
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
                amount=reservation_price,
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
            payment.save()

            reservation = Reservation.objects.get(id=reservation_id)
            reservation.paymentStatus = 'Payed'
            reservation.save()

            email_data = {
                'nursery': nursery,
                'reservation': reservation,
                'payment': payment
            }
            send_email(email_data)
            return redirect('reservation:ReservationCompleted', reservation_id)
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
        'description': description,
        'payment_exist': payment_exist
    }
    return render(request, 'reservation/transaction.html', context)


def send_email(email_data):
    reservation = email_data['reservation']
    payment = email_data['payment']
    try:
        subject = "Travel Sitter - Reservation #{}".format(reservation.id)
        to_email = ['{}'.format(payment.emailAddress)]
        from_email = "orders@travelsitter.com"
        message = get_template('email.html').render(email_data)
        msg = EmailMessage(subject, message, from_email, to_email)
        msg.content_subtype = 'html'
        msg.send()
        print('The order email has been sent to the customer.')
    except IOError as e:
        return e


def reservation_completed(request, reservation_id):
    context = {
        'reservation_id': reservation_id
    }
    return render(request, 'reservation/completed.html', context)


@login_required
def history_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    context = {
        'reservations': reservations
    }
    return render(request, 'reservation/history_list.html', context)


def history_detail(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        reservation = None

    try:
        nursery = Nursery.objects.get(id=reservation.nursery_id)
    except Nursery.DoesNotExist:
        nursery = None

    try:
        payment = Payment.objects.get(reservation=reservation)
    except Payment.DoesNotExist:
        payment = None

    context = {
        'reservation': reservation,
        'nursery': nursery,
        'payment': payment
    }
    return render(request, 'reservation/history_detail.html', context)


def get_stock_per_date(request):
    target_date = request.GET.get('target_date', None)
    nursery_id = request.GET.get('nursery_id', None)

    nursery = Nursery.objects.get(id=nursery_id)
    reservations = Reservation.objects.filter(nursery=nursery, start_date=target_date)
    reserved_child_number = 0
    for reservation in reservations:
        reserved_child_number += reservation.child_number
    available_stock = nursery.stock - reserved_child_number

    data = {
        'stock': available_stock
    }

    return JsonResponse(data)
