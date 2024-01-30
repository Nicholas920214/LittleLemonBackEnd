# from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json

from .forms import BookingForm

# csrf tokem
from django.views.decorators.csrf import csrf_exempt

# API
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import MenuSerializer, BookingSerializer


# API views
# If need authentication, use insomnia to retrieve the data


class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]  # need authentication
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


# Latter inspect, sth problems
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


# Using viewset, later inspect
class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # need authentication
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# Page views
def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def book(request):
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, "book.html", context)


# Add code for the bookings() view
def reservations(request):
    date = request.GET.get("date", datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize("json", bookings)
    bookings_data = {"bookings": bookings}
    return render(request, "bookings.html", {"bookings": bookings_data})


# bookings url is entirely for the json format website, no html and css styling
@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)
        exist = (
            Booking.objects.filter(reservation_date=data["reservation_date"])
            .filter(reservation_slot=data["reservation_slot"])
            .exists()
        )
        if exist == False:
            booking = Booking(
                first_name=data["first_name"],
                reservation_date=data["reservation_date"],
                reservation_slot=data["reservation_slot"],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type="application/json")

    date = request.GET.get("date", datetime.today().date())
    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize(
        "json", bookings
    )  # json serializers is in django.cores# If using this, then the data cannot be passed
    # return render(
    #    request, "bookings.html", {"bookings": booking_json}
    # )  # the bookings key will pass into bookings.html

    # return the json format data
    return HttpResponse(booking_json, content_type="application/json")


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, "menu.html", {"menu": main_data})


def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, "menu_item.html", {"menu_item": menu_item})
