from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import City,Nursery
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


def index(request):
    text_var = 'Start!!!'
    return HttpResponse(text_var)


def allCity(request, c_slug=None):
    c_page = None
    cities_list = None
    if c_slug!=None:
        c_page = get_object_or_404(City,slug=c_slug)
        cities_list = City.objects.filter(city=c_page)
    else:
        cities_list = City.objects.all()
    paginator = Paginator(cities_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        cities = paginator.page(page)
    except (EmptyPage,InvalidPage):
        cities = paginator.page(paginator.num_pages)

    return render(request, 'service/category.html', {'cities': cities})


def allSitting(request, c_slug=None):
    c_page = None
    sittings_list = None
    if c_slug is not None:
        c_page = get_object_or_404(City, slug=c_slug)
        sittings_list = Nursery.objects.filter(city=c_page, available=True)
    else:
        sittings_list = Nursery.objects.all().filter(available=True)
    paginator = Paginator(sittings_list, 6)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        sittings = paginator.page(page)
    except (EmptyPage,InvalidPage):
        sittings = paginator.page(paginator.num_pages)
    return render(request,'service/city.html',{'city':c_page, 'sittings':sittings})


def SittingDetail(request, c_slug, nursery_slug):
    try:
        nursery = Nursery.objects.get(city__slug=c_slug, slug=nursery_slug)
    except Exception as e:
        raise e
    return render(request, 'service/nursery.html', {'nursery': nursery})


def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form':form})


def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('service:allCity')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/signin.html', {'form': form})


def signoutView(request):
    logout(request)
    return redirect('signin')
