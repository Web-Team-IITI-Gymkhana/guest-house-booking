from django.contrib import admin
from .models import BookingStatus
from Rooms.models import Room


# Register your models here.

class Filtern(admin.ModelAdmin):
    list_display=("booked_by","start_date","end_date")
    list_filter=("is_accepted",)
admin.site.register(BookingStatus,Filtern)




# class Filter(admin.ModelAdmin):
#     list_display=("room_no","location","status")
#     list_filter=("is_available","room_type")
# admin.site.register(Room,Filter)


# class newadminarea(admin.AdminSite):
#     site_header='new admin login'
# class Filter(admin.ModelAdmin):
#     list_display=("location","status")
#     list_filter=("room_type")
# book_site=newadminarea(name='newadmin')

# book_site.register(Room,Filter)
# book_site.register(ResidentDetails,Filter)



# from django.contrib import admin
# from .models import BookingStatus, ResidentDetails
# from Rooms.models import Room

# class newadminarea(admin.AdminSite):
#     site_header = 'new admin login'
# book_site = newadminarea(name='newadmin')


# class Filter_available(admin.ModelAdmin):
#     list_filter = ("room_no__room_type", "is_accepted")

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs

#     def get_list_display(self, request):
#         # Check if filtering by room_type
#         if 'room_no__room_type' in request.GET:
#             self.list_display = ("room_no", "is_available")  # Customize list_display for room_type filter
#         else:
#             self.list_display = ("booked_by", "reason", "is_accepted", "room_no")  # Default list_display for other filters







# book_site.register(BookingStatus, Filter_available)
# book_site.register(ResidentDetails, Filter)

