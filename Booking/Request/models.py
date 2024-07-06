from django.db import models
from datetime import datetime
from Rooms.models  import Room 
from BookStatus.models  import BookingStatus  
import uuid
from django.db import models
from django.conf import settings
# # from django.db import models

# # # Create your models here.
# # class Request(models.Model):
# #     room_choices=(
# #         ('YAC','AC'),
# #         ( 'NAC','NON-AC'),
# #     )
# #     first_name=models.CharField(max_length=40)
# #     last_name=models.CharField(max_length=40)
# #     email=models.EmailField()
# #     contact=models.CharField(max_length=40)
# #     number_guest=models.IntegerField()
# #     reason=models.CharField(max_length=40)
# #     check_in=models.DateField()
# #     check_out=models.DateField()
# #     available_rooms   =  models.CharField(max_length=40, choices=room_choices)


# from django.db import models
# from datetime import datetime
# # from BookStatus.functions.availability import check_availability,update_room_availability

# class Request(models.Model):
    
#     first_name = models.CharField(max_length=40)
#     last_name = models.CharField(max_length=40)
#     email = models.EmailField()
#     contact = models.CharField(max_length=40)
#     number_guest = models.IntegerField()
#     reason = models.CharField(max_length=40)
#     check_in = models.DateField()
#     check_out = models.DateField()

class Request(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    contact = models.CharField(max_length=40)
    number_guest = models.IntegerField()
    reason = models.CharField(max_length=40)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, default='Pending')  
    # statussssss = models.CharField(max_length=20, default='Pending')  
  
    
    

    def get_available_rooms(self):
        available_rooms = []
        rooms = Room.objects.filter(is_available=True)
        print(self.check_in,self.check_out)
        for room in rooms:
            print(room)
            if self.check_availability(room, self.check_in, self.check_out):
                
                available_rooms.append({
                    'room_no': room.room_no,
                    'type': room.room_type,
                    'location': room.location
                })
        return available_rooms

    def check_availability(self, room_no, check_in, check_out):
        bookings = BookingStatus.objects.filter(room_no=room_no)
        print(bookings)
        for booking in bookings:
            
            if booking.start_date and booking.end_date:
                if not (booking.start_date > check_out or booking.end_date < check_in):
                    print(booking.start_date,booking.end_date,"false")
                    return False
            print(booking.start_date,booking.end_date,"true")
        return True
    
    class Meta:
        verbose_name = "Requests"
        verbose_name_plural = "Requests"


    def str(self):
        return f"{self.first_name} {self.last_name} - {self.check_in} to {self.check_out}"