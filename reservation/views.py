from django.shortcuts import render, redirect, get_object_or_404
from service.models import Nursery
from .models import Reservation, ReservationItem, ReservationInfomation
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from order.models import Order, OrderItem
from django.template.loader import get_template
from django.core.mail import EmailMessage
from .forms import ReservationInfoForm
from django.http import HttpResponse


def _reservation_id(request):
    reservation = request.session.session_key
    if not reservation:
        reservation = request.session.create()
    return reservation


def _reservationinfomation_id(request):
    reservationinfomation = request.session.session_key
    if not reservationinfomation:
        reservationinfomation = request.session.create()
    return reservationinfomation


def add_reservation(request, nursery_id):
    nursery = Nursery.objects.get(id=nursery_id)
    try:
        reservation = Reservation.objects.get(reservation_id=_reservation_id(request))
    except Reservation.DoesNotExist:
        reservation = Reservation.objects.create(
            reservation_id=_reservation_id(request)
        )
        reservation.save()
    try:
        reservation_item = ReservationItem.objects.get(nursery=nursery, reservation=reservation)
        if reservation_item.quantity < reservation_item.nursery.stock:
            reservation_item.quantity += 1
        reservation_item.save()
    except ReservationItem.DoesNotExist:
        reservation_item = ReservationItem.objects.create(
            nursery=nursery,
            quantity=1,
            reservation=reservation
        )
        reservation_item.save()
    return redirect('reservation:reservation_detail', nursery_id)


def reservation_detail(request, nursery_id, total=0, counter=0, cart_items = None):
    reservation_items = []
    try:
        reservation = Reservation.objects.get(reservation_id=_reservation_id(request))
        reservation_items = ReservationItem.objects.filter(reservation=reservation, active=True)
        for reservation_item in reservation_items:
            total += (reservation_item.nursery.price * reservation_item.quantity)
            counter += reservation_item.quantity
    except ObjectDoesNotExist:
        pass
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Travel Sitter - Reserve'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        #  print(request.POST)
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
          
            try:
                order_details = Order.objects.create(
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
                    nursery_id=nursery_id
                )
                order_details.save()
                for order_item in reservation_items:
                    oi = OrderItem.objects.create(
                        nursery=order_item.nursery.name,
                        quantity=order_item.quantity,
                        price=order_item.nursery.price,
                        order=order_details
                    )
                    oi.save()
                 
                    nurseries = Nursery.objects.get(id=order_item.nursery.id)
                    nurseries.stock = int(order_item.nursery.stock - order_item.quantity)
                    nurseries.save()
                    order_item.delete()
                 
                    print('The Reservation has been created')
                # try:
                #     send_email(order_details.id)
                #     print('The order email has been sent to the customer.')
                # except IOError as e:
                #     return e

                order_details_id = order_details.id
                return redirect('reservation:reservation_new', order_details_id)
                # return redirect('order:thanks', order_details.id)
            except ObjectDoesNotExist:
                pass 
          
        except stripe.error.CardError as e:
            return False, e
    return render(request, 'reservation.html', dict(reservation_items=reservation_items, total=total, counter=counter, data_key=data_key, stripe_total=stripe_total, description=description))
  

def reservation_new(request, order_details_id):
    transaction = Order.objects.get(id=order_details_id)
    order_items = OrderItem.objects.filter(order=transaction)
    nursery = Nursery.objects.get(id=transaction.nursery_id)

    form = ReservationInfoForm(request.POST or None)   
    if form.is_valid():
        reservation_information = ReservationInfomation()
        reservation_information.rtime = form.cleaned_data['rtime']
        reservation_information.your_name = form.cleaned_data['your_name']
        reservation_information.email = form.cleaned_data['email']
        reservation_information.reservation_date = form.cleaned_data['reservation_date']
        reservation_information.age_ofthechild = form.cleaned_data['age_ofthechild']
        reservation_information.allergies = form.cleaned_data['allergies']
        reservation_information.vaccinations = form.cleaned_data['vaccinations']
        reservation_information.illness = form.cleaned_data['illness']
        reservation_information.travel_insurance = form.cleaned_data['travel_insurance']
        reservation_information.wifi = form.cleaned_data['wifi']
        reservation_information.note = form.cleaned_data['note']
        
        ReservationInfomation.objects.create(
            rtime=reservation_information.rtime,
            your_name=reservation_information.your_name,
            email=reservation_information.email,
            reservation_date=reservation_information.reservation_date,
            age_ofthechild=reservation_information.age_ofthechild,
            allergies=reservation_information.allergies,
            vaccinations=reservation_information.vaccinations,
            illness=reservation_information.illness,
            travel_insurance=reservation_information.travel_insurance,
            wifi=reservation_information.wifi,
            note=reservation_information.note,
        )

        data = {
            'transaction': transaction,
            'order_items': order_items,
            'nursery': nursery,
            'reservation_information': reservation_information
        }

        send_email(data)

        return redirect('reservation:thankyou')
    '''
        try:
            confEmail(reservation_information.email)
            print('The confirm email has been sent to the customer.')   
        except IOError as e:
            return e 
        return redirect('reservation:reservation_new')
    
    '''

    return render(request, 'reservation_new.html', {'form': form})


def thankyou(request):
    text_var = 'Thank you for your making reservation. We sent you an Email. Please confirm it.'
    return HttpResponse(text_var)


def send_email(data):
    # transaction = Order.objects.get(id=order_id)
    # order_items = OrderItem.objects.filter(order=transaction)
    # now_nursery = Nursery.objects.get(id=Nursery.nursey_id)
    # order_information = {
    #     'transaction': transaction,
    #     'order_items': order_items,
    #     # 'now_nursery' : now_nursery,
    # }

    transaction = data['transaction']
    try:
        subject = "Travel Sitter - Reservation #{}".format(transaction.id)
        to_email = ['{}'.format(transaction.emailAddress)]
        from_email = "orders@travelsitter.com"
        message = get_template('email/email.html').render(data)
        msg = EmailMessage(subject, message, from_email, to_email)
        msg.content_subtype = 'html'
        msg.send()
    except IOError as e:
        return e


# def confEmail(reservationinfomation):
#     trans = ReservationInfomation.objects.get(email=reservationinfomation.email)
#     try:
#             subject = "Travel Sitter - Reservation confirm"
#             to = ['{}'.format(trans.email)]
#             from_email = "orders@travelsitter.com"
#             reservationinfomation_infomation = {
#                 'trans': trans
#             }
#             message = get_template('email/reservationinfomation.html').render(reservationinfomation_infomation)
#             msg = EmailMessage(subject, message, to=to, from_email=from_email)
#             msg.content_subtype = 'html'
#             msg.send()
#     except IOError as e:
#         return e


def reservation_remove(request, nursery_id):
    reservation = Reservation.objects.get(reservation_id=_reservation_id(request))
    nursery = get_object_or_404(Nursery, id=nursery_id)
    reservation_item = ReservationItem.objects.get(nursery=nursery, reservation=reservation)
    if reservation_item.quantity > 1:
        reservation_item.quantity -= 1
        reservation_item.save()
    else:
        reservation_item.delete()
    return redirect('reservation:reservation_detail', nursery_id)


def full_remove(request, nursery_id):
    reservation = Reservation.objects.get(reservaton_id=_reservation_id(request))
    nursery = get_object_or_404(Nursery, id=nursery_id)
    reservation_item = ReservationItem.objects.get(nursery=nursery, reservation=reservation)
    reservation_item.delete()
    return redirect('reservation:reservation_detail', nursery_id)
