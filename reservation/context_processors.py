from .models import Reservation, ReservationItem
from .views import _reservation_id

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            reservation = Reservation.objects.filter(reservation_id=_reservation_id(request))
            reservation_items = ReservationItem.objects.all().filter(reservation=reservation[:1])
            for reservation_item in reservation_items:
                item_count += reservation_item.quantity
        except Reservation.DoesNotExist:
            item_count = 0
    return dict(item_count = item_count)