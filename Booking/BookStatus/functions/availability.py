# from datetime import datetime
# from BookStatus.models import BookingStatus
# from Rooms.models import Room

# def check_availability(room, check_in, check_out):
#     booking_list = BookingStatus.objects.filter(room_no=room)
#     for booking in booking_list:
#         if booking.start_date and booking.end_date:
#             if not (booking.start_date > check_out or booking.end_date < check_in):
#                 return False
#     return True

# def update_room_availability(check_in, check_out):
#     room_list = []
#     rooms = Room.objects.all()
#     for room in rooms:
#         if check_availability(room.room_no, check_in=check_in, check_out=check_out):
#             room.is_available = True
#             room_list.append(room)
#         else:
#             room.is_available = False
#         room.save()
#     return room_list
from datetime import datetime
from BookStatus.models import BookingStatus
from Rooms.models import Room

def check_availability(room_no, check_in, check_out):
    booking_list = BookingStatus.objects.filter(room_no=room_no)
    for booking in booking_list:
        if booking.start_date and booking.end_date:
            if  (booking.start_date > check_out or booking.end_date < check_in):
                return True
    return False
# req
def get_available_rooms(check_in, check_out):
    available_rooms = []
    rooms = Room.objects.filter(is_available=True)
    for room in rooms:
        if check_availability(room.room_no, check_in, check_out):
            available_rooms.append({
                'room_no': room.room_no,
                'type': room.room_type,
                'location': room.location
            })
    return available_rooms