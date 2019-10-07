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
                       reservation_id = _reservation_id(request)
         )
        reservation.save()
    try:
        reservation_item = ReservationItem.objects.get(nursery=nursery, reservation=reservation)
        if reservation_item.quantity < reservation_item.nursery.stock:
            reservation_item.quantity += 1
        reservation_item.save()
    except ReservationItem.DoesNotExist:
        reservation_item = ReservationItem.objects.create(
                           nursery = nursery,
                           quantity = 1,
                           reservation = reservation     
             )
        reservation_item.save()
    return redirect('reservation:reservation_detail')

def reservation_detail(request, total=0, counter=0, cart_items = None):
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
                        source = token
                )
            charge = stripe.Charge.create(
                        amount=stripe_total,
                        currency="usd",
                        description=description,
                        customer=customer.id
                )
          
            try:
                order_details = Order.objects.create(
                        token = token,
                        total = total,
                        emailAddress = email,
                        billingName = billingName,
                        billingAddress1 = billingAddress1,
                        billingCity = billingcity,
                        billingPostcode = billingPostcode,
                        billingCountry = billingCountry,
                        shippingName = shippingName,
                        shippingAddress1 = shippingAddress1,
                        shippingCity = shippingcity,
                        shippingPostcode = shippingPostcode,
                        shippingCountry = shippingCountry
                    )
                order_details.save()
                for order_item in reservation_items:
                    oi = OrderItem.objects.create(
                            nursery = order_item.nursery.name,
                            quantity = order_item.quantity,
                            price = order_item.nursery.price,
                            order = order_details 
                        )
                    oi.save()
                 
                    nurseries = Nursery.objects.get(id=order_item.nursery.id)
                    nurseries.stock = int(order_item.nursery.stock - order_item.quantity)
                    nurseries.save()
                    order_item.delete()
                 
                    print('The Reservation has been created')
                try:
                    sendEmail(order_details.id)
                    print('The order email has been sent to the customer.')   
                except IOError as e:
                    return e 
                return redirect('reservation:reservation_new')
               # return redirect('order:thanks', order_details.id)
            except ObjectDoesNotExist:
                pass 
          
        except stripe.error.CardError as e:
            return False,e
    return render(request, 'reservation.html', dict(reservation_items = reservation_items, total = total, counter = counter, data_key = data_key, stripe_total = stripe_total, description = description))
  

def reservation_remove(request, nursery_id):
    reservation = Reservation.objects.get(reservation_id=_reservation_id(request))
    nursery = get_object_or_404(Nursery, id=nursery_id)
    reservation_item = ReservationItem.objects.get(nursery=nursery, reservation=reservation)
    if reservation_item.quantity > 1:
        reservation_item.quantity -= 1
        reservation_item.save()
    else:
        reservation_item.delete()
    return redirect('reservation:reservation_detail')  


def full_remove(request, nursery_id):
    reservation = Reservation.objects.get(reservaton_id=_reservation_id(request))
    nursery = get_object_or_404(Nursery, id=nursery_id)
    reservation_item = ReservationItem.objects.get(nursery=nursery, reservation=reservation)
    reservation_item.delete()
    return redirect('reservation:reservation_detail')

def sendEmail(order_id):
    transaction = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=transaction)
  #  now_nursery = Nursery.objects.get(id=Nursery.nursey_id)
    try:
        subject = "Travel Sitter - Reservation #{}".format(transaction.id)
        to = ['{}'.format(transaction.emailAddress)]
        from_email = "orders@travelsitter.com"
        order_information = {
        'transaction' : transaction,
        'order_items' : order_items,
      #  'now_nursery' : now_nursery,                      
        }
        message = get_template('email/email.html').render(order_information)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
    except IOError as e:
        return e
    
def reservation_new(request):
  #  reservationinfomation_id=_reservationinfomation_id(request)
    form = ReservationInfoForm(request.POST or None)   
    if form.is_valid():
        reservationinfomation = ReservationInfomation()
        reservationinfomation.rtime = form.cleaned_data['rtime']
        reservationinfomation.your_name = form.cleaned_data['your_name']
        reservationinfomation.email = form.cleaned_data['email']
        reservationinfomation.reservation_date = form.cleaned_data['reservation_date']
        reservationinfomation.age_ofthechild = form.cleaned_data['age_ofthechild']
        reservationinfomation.allergies = form.cleaned_data['allergies']
        reservationinfomation.vaccinations = form.cleaned_data['vaccinations']
        reservationinfomation.illness = form.cleaned_data['illness']
        reservationinfomation.travel_insurance = form.cleaned_data['travel_insurance']
        reservationinfomation.wifi = form.cleaned_data['wifi']
        reservationinfomation.note = form.cleaned_data['note']
        
        ReservationInfomation.objects.create(
            rtime=reservationinfomation.rtime,
            your_name=reservationinfomation.your_name,
            email=reservationinfomation.email,
            reservation_date=reservationinfomation.reservation_date,
            age_ofthechild=reservationinfomation.age_ofthechild,
            allergies=reservationinfomation.allergies,
            vaccinations=reservationinfomation.vaccinations,
            illness=reservationinfomation.illness,
            travel_insurance=reservationinfomation.travel_insurance,
            wifi=reservationinfomation.wifi,
            note=reservationinfomation.note,
        )
        return redirect('reservation:thankyou') 
    '''
        try:
            confEmail(reservationinfomation.email)
            print('The confirm email has been sent to the customer.')   
        except IOError as e:
            return e 
        return redirect('reservation:reservation_new')
    
        '''

    return render(request, 'reservation_new.html', {'form': form})


def thankyou(request):
    text_var = 'Thank you for your making reservation. We sent you an Email. Please confirm it.'
    return HttpResponse(text_var)

def confEmail(reservationinfomation):
    trans = ReservationInfomation.objects.get(email=reservationinfomation.email)
    try:
            subject = "Travel Sitter - Reservation confirm"
            to = ['{}'.format(trans.email)]
            from_email = "orders@travelsitter.com"
            reservationinfomation_infomation = {
            'trans' : trans       
            }
            message = get_template('email/reservationinfomation.html').render(reservationinfomation_infomation)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
    except IOError as e:
        return e