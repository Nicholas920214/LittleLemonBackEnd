from django.forms import ModelForm
from .models import Booking


# Code added for loading from data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
