from django.db import models
# Create your models here.
class Room(models.Model):
    ROOM_TYPE=(
        ('YAC','AC'),
        ( 'NAC','NON-AC'),
    )
    room_no     =  models.IntegerField()
    location    =  models.CharField(max_length=40)
    status      =  models.BooleanField()
    room_type   =  models.CharField(max_length=40, choices=ROOM_TYPE)
    