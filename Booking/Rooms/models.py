
from django.db import models
# Create your models here.
class Room(models.Model):
    ROOM_TYPE=(
        ('YAC','AC'),
        ( 'NAC','NON-AC'),
    )
    room_no     =  models.IntegerField()
    location    =  models.CharField(max_length=40)
    # status      =  models.BooleanField()
    room_type   =  models.CharField(max_length=40, choices=ROOM_TYPE)
    is_available=  models.BooleanField(default=True)

    class Meta:
        verbose_name = "Rooms"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f'room no. is {self.room_no} in {self.location} type {self.room_type} '
    