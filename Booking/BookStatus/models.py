from django.db import models
# from ..Rooms import Room
from Rooms.models import Room

# Create your models here.
class BookingStatus(models.Model):
    room_no      =  models.ForeignKey(Room,default=None,on_delete=models.SET_DEFAULT)
    booked_by    =  models.CharField(max_length=50)
    start_date   =  models.DateField()
    end_date     =  models.DateField()
    booked_on    =  models.DateField()
    reason       =  models.TextField(max_length=50)
    checked_in   =  models.DateField()
    is_accepted  =  models.BooleanField()


class ResidentDetails(models.Model):
    resident_name    =  models.ForeignKey(BookingStatus,default=None,on_delete=models.SET_DEFAULT)
    e_mail           =  models.CharField(max_length=40)
    phone_no         =  models.IntegerField(max_length=10)
    

    