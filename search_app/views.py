from django.shortcuts import render
from service.models import City
from django.db.models import Q


def searchResult(request):
    cities = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        # cities = City.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
        cities = City.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'search.html', {'query': query, 'cities': cities})
