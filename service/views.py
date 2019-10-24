from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from .forms import SignUpForm, NurseryForm
from .models import City, Nursery


def index(request):
    pass


def all_city(request, c_slug=None):
    if c_slug is not None:
        c_page = get_object_or_404(City, slug=c_slug)
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
    except (EmptyPage, InvalidPage):
        cities = paginator.page(paginator.num_pages)

    return render(request, 'service/all_city.html', {'cities': cities})


def city_detail(request, c_slug=None):
    c_page = None
    if c_slug is not None:
        c_page = get_object_or_404(City, slug=c_slug)
        nursery_list = Nursery.objects.filter(city=c_page, available=True)
    else:
        nursery_list = Nursery.objects.all().filter(available=True)
    paginator = Paginator(nursery_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        nursery = paginator.page(page)
    except (EmptyPage, InvalidPage):
        nursery = paginator.page(paginator.num_pages)
    return render(request, 'service/city.html', {'city': c_page, 'nursery': nursery})


def nursery_detail(request, c_slug, nursery_slug):
    current_user = request.user
    show_alert = False
    if current_user.is_authenticated is False:
        show_alert = True
    else:
        user_type = current_user.groups.get(user=current_user).name
        if user_type == 'Vendor':
            show_alert = True

    try:
        nursery = Nursery.objects.get(city__slug=c_slug, slug=nursery_slug)
        nursery.id = int(nursery.id)
        nursery.price_plan = json.loads(nursery.price_plan)
        nursery_id = int(nursery.id)

    except Exception as e:
        raise e

    context = {
        'nursery': nursery,
        'nursery_id': nursery_id,
        'show_alert': show_alert
    }
    return render(request, 'service/nursery.html', context)


@login_required
def vendor_dashboard(request):
    current_user = request.user
    nursery_user_exist = False

    if request.method == 'POST':
        nursery_form = NurseryForm(request.POST, request.FILES)
        if nursery_form.is_valid():
            name = nursery_form.cleaned_data['name']
            slug = nursery_form.cleaned_data['slug']
            description = nursery_form.cleaned_data['description']
            address = nursery_form.cleaned_data['address']
            telephone = nursery_form.cleaned_data['telephone']
            station = nursery_form.cleaned_data['station']
            # price = 500
            image = nursery_form.cleaned_data['image']
            stock = nursery_form.cleaned_data['stock']
            city = City.objects.get(id=nursery_form.cleaned_data['city'])

            price_plan = []
            time_one = nursery_form.cleaned_data['time_one']
            price_one = nursery_form.cleaned_data['price_one']
            time_two = nursery_form.cleaned_data['time_two']
            price_two = nursery_form.cleaned_data['price_two']
            time_three = nursery_form.cleaned_data['time_three']
            price_three = nursery_form.cleaned_data['price_three']

            if time_one != '' and price_one != '':
                price_plan.append({'time': time_one, 'price': price_one})
            if time_two != '' and price_two != '':
                price_plan.append({'time': time_two, 'price': price_two})
            if time_three != '' and price_three != '':
                price_plan.append({'time': time_three, 'price': price_three})

            price_plan = json.dumps(price_plan)

            try:
                nursery = Nursery.objects.get(Q(name=name) | Q(slug=slug))

                nursery.name = nursery_form.cleaned_data['name']
                nursery.slug = nursery_form.cleaned_data['slug']
                nursery.description = nursery_form.cleaned_data['description']
                nursery.address = nursery_form.cleaned_data['address']
                nursery.telephone = nursery_form.cleaned_data['telephone']
                nursery.station = nursery_form.cleaned_data['station']
                # nursery.price = price
                nursery.price_plan = price_plan
                if nursery_form.cleaned_data['image'] is not None:
                    if nursery_form.cleaned_data['image'] is False:
                        nursery.image = ''
                    else:
                        nursery.image = nursery_form.cleaned_data['image']
                nursery.stock = nursery_form.cleaned_data['stock']
                nursery.city = City.objects.get(id=nursery_form.cleaned_data['city'])
                nursery.user = current_user

                nursery.save()
                return redirect('service:VendorDashboard')
            except Nursery.DoesNotExist:
                try:
                    Nursery.objects.get(user=current_user)
                    nursery_user_exist = True
                except Nursery.DoesNotExist:
                    Nursery.objects.create(
                        name=name,
                        slug=slug,
                        description=description,
                        address=address,
                        telephone=telephone,
                        station=station,
                        # price=price,
                        price_plan=price_plan,
                        image=image,
                        stock=stock,
                        city=city,
                        user=current_user
                    )
                    return redirect('service:VendorDashboard')

    else:
        nursery_form = NurseryForm()

        try:
            nursery = Nursery.objects.get(user=current_user)

            nursery_form.initial = {
                'name': nursery.name,
                'slug': nursery.slug,
                'description': nursery.description,
                'address': nursery.address,
                'telephone': nursery.telephone,
                'station': nursery.telephone,
                'image': nursery.image,
                'stock': nursery.stock,
                'city': nursery.city_id
            }

            price_plan = json.loads(nursery.price_plan)
            if price_plan is not None:
                for x in range(len(price_plan)):
                    price_plan_dict = price_plan[x]
                    if x == 0:
                        nursery_form.initial['time_one'] = price_plan_dict['time']
                        nursery_form.initial['price_one'] = price_plan_dict['price']
                    elif x == 1:
                        nursery_form.initial['time_two'] = price_plan_dict['time']
                        nursery_form.initial['price_two'] = price_plan_dict['price']
                    elif x == 2:
                        nursery_form.initial['time_three'] = price_plan_dict['time']
                        nursery_form.initial['price_three'] = price_plan_dict['price']
        except Nursery.DoesNotExist:
            pass

    context = {
        'nursery_form': nursery_form,
        'nursery_user_exist': nursery_user_exist
    }
    return render(request, 'service/vendor_dashboard.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_type = form.cleaned_data.get('user_type')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name=user_type)
            user_group.user_set.add(signup_user)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('service:AllCity')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/signin.html', {'form': form})


def signoutView(request):
    logout(request)
    return redirect('signin')
