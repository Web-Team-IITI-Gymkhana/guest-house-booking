from django.contrib import admin
from .models import BookingStatus
from Rooms.models import Room


# Register your models here.

class Filtern(admin.ModelAdmin):
    list_display=("booked_by","start_date","end_date","room_no")
    list_filter=("is_accepted",)
admin.site.register(BookingStatus,Filtern)