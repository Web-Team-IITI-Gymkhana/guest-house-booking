from django.db import models
# from ..Rooms import Room
from Rooms.models import Room
# from BookStatus.models import BookingStatus
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



# Create your models here.
class BookingStatus(models.Model):
    room_no      =  models.ForeignKey(Room,on_delete=models.SET_DEFAULT,default=None,null=True)
    booked_by    =  models.CharField(max_length=50)
    start_date   =  models.DateField()
    end_date     =  models.DateField()
    booked_on    =  models.DateField(auto_now_add=True)
    reason       =  models.TextField(max_length=50)
    checked_in   =  models.BooleanField(default=False)
    checked_out  =  models.BooleanField(default=False)
    is_accepted  =  models.BooleanField(default=False)
    e_mail       =  models.CharField(max_length=40,default=False)
    phone_no     =  models.IntegerField(default=False)
    

    def _str_(self):
        return f"{self.booked_by} - {self.room_no}"
    
    class Meta:
            verbose_name = "Booking Status"
            verbose_name_plural = "Booking Status"



