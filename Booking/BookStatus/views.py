from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.forms import ModelForm
from django.contrib.auth import authenticate,login as auth_login,logout
from BookStatus.models import BookingStatus
from Rooms.models import Room
# from BookStatus.models import ResidentDetails
from .forms import bookingForm
from datetime import datetime
from django.db.models import Q
from django.views.generic import ListView,FormView
from django.contrib import messages
from BookStatus.functions.availability import get_available_rooms,check_availability    
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import admin
from django.http import HttpResponse
from .models import Room
from Request.models import Request
from django.core.mail import send_mail

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User=get_user_model()
def signup(request):
    if(request.method=="POST"):
        lname=request.POST.get('lname')
        fname=request.POST.get('fname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if User.objects.filter(email=email):
            messages.error(request,"email already exists!! Sign-In or use another e-mail")
            return render(request,'account/signup.html',
                            {'fname':fname,
                             'lname':lname
                             }
                            )
        if pass1 != pass2 :
            messages.error(request,"passwords do not match!!! Try again")

            return render(request,'account/signup.html',
                            {'fname':fname,
                             'lname':lname,
                             'email':email
                             }
                            )
        else:

            myuser=User.objects.create_user(email,email,pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()

            # welcome message
            subject= "welcome to guesthouse booking login"
            message="hello"+myuser.first_name + " !! \n"+ "welcome to gfg!! "
            from_email= settings.EMAIL_HOST_USER
            to_list=[myuser.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)
            return redirect('login')

    return render(request,'account/signup.html')

def login(request):
    if(request.method=="POST"):
        email=request.POST.get('email')
        pass1=request.POST.get('pass')
        user=authenticate(email=email, password=pass1)
        if user is not None:
            auth_login(request,user)
            fname=user.first_name
            return render(request,'main.html',{'fname':fname})
        else:
            messages.error(request,"invalid credentials")
            return redirect('login')


    return render(request,'account/login.html')

def main(request):
    return render(request,'main.html')


# def request_list(request):
    # requests = Request.objects.all()
    # return render(request, 'request_list.html', {'requests': requests})



# @admin.register(Request)
# class RequestAdmin(admin.ModelAdmin):
#     change_list_template = 'templates/request_list.html'

#     def changelist_view(self, request, extra_context=None):
#         extra_context = extra_context or {}
#         print("hi", request.GET)
#         requests_all = Request.objects.all()
#         available_rooms_list = []
#         for r in requests_all:
#             check_in = r.check_in
#             check_out = r.check_out
#             if check_in and check_out:
#                 available_rooms = get_available_rooms(check_in, check_out)
#                 print(check_in,check_out)
#                 available_rooms_list.append(available_rooms)
#                 print(available_rooms)
#                 print(available_rooms_list)
                
        
#         extra_context['available_rooms'] = available_rooms_list
#         extra_context['requests'] = requests_all
        
#         return super().changelist_view(request, extra_context=extra_context)

@admin.register(Request)

class RequestAdmin(admin.ModelAdmin):
    change_list_template = 'templates/request_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        requests_all = Request.objects.all()
        
        # Prepare data for each request
        request_data = []
        for r in requests_all:
            available_rooms = Room.objects.all()
            bookings=BookingStatus.objects.all()
            request_data.append({
                'request': r,
                'available_rooms': available_rooms,
                'bookings': bookings
            })
            print(available_rooms,r.first_name,r.last_name)
       
        
        extra_context['request_data'] = request_data
        return super().changelist_view(request, extra_context=extra_context)


# @admin.register(Request)
# class RequestAdmin(admin.ModelAdmin):
#     change_list_template = 'templates/request_list.html'

#     def changelist_view(self, request, extra_context=None):
#         extra_context = extra_context or {}
#         print("hi",request.GET)
#         requests_all =Request.objects.all()
#         for r in requests_all:
#             check_in=r.check_in
#             check_out=r.check_out
#             if check_in and check_out:
#                 available_rooms = get_available_rooms(check_in, check_out)
#                 extra_context['available_rooms'] = available_rooms
#             extra_context['requests'] = r
#             return super().changelist_view(request, extra_context=extra_context)
 

# @admin.register(Request)
# class RequestAdmin(admin.ModelAdmin):
#     change_list_template = 'templates/request_list.html'

#     def changelist_view(self, request, extra_context=None):
#         # Get the existing context from the changelist_view
#         extra_context = extra_context or {}
#         # available_rooms=get_available_rooms(request.check_in, request.check_out)

#         extra_context['requests'] = Request.objects.all()
#         # extra_context['available_rooms'] = available_rooms
#         return super(RequestAdmin, self).changelist_view(request, extra_context=extra_context)





# def booking(request):
#     return render(request,"bookingform.html")

class RoomList(ListView):
     model=Room
class BookingList(ListView):
     model=BookingStatus
     
# def save_bookingform(request):
#     form = bookingForm() 
#     if request.method=='POST':
        
        
#             form = bookingForm(request.POST) 
#             fname=request.POST.get('first_name')
#             lname=request.POST.get('last_name')
#             email=request.POST.get('email')
#             location=request.POST.get('location')
#             check_in=request.POST.get('check_in')
#             check_out=request.POST.get('check_out')
#             reason=request.POST.get('reason')
#             booked_by = f"{fname} {lname}" 
#             # class ArticleForm(ModelForm):
#             #     class Meta:
#             #         model = ResidentDetails
#             #         fields = "all"
#             # rform = ArticleForm()
            
#             instance=BookingStatus.objects.create(
#                 # room_no=rform,
#                 booked_by=fname,
#                 start_date=check_in,
#                 end_date=check_out,
#                 reason=reason
#             )
#             instance.save()
#             print("hii")
            
#             return render(request, "main.html")
        

    
#     else:
#         return render(request, 'bookingform.html', {'form':bookingForm()})

# class BookingView(FormView):
#     form_class=bookingForm
#     template_name='availability_form.html'

#     def form_valid(self,form):
#         data=form.cleaned_data
#         room_list=Room.objects.all
#         available_rooms=[]
#         for room in room_list:
#             if check_availability(room,data['check_in'],data['check_out']):
#                 available_rooms.append(room)
#         if len(available_rooms)>0:    
#             room=available_rooms[0]
#             booking=BookingStatus.objects.create(
#                 booked_by=data['first_name'],
#                 room_no=room,
#                 start_date=data['check_in'],
#                 end_date=data['check_out'],
#                 reason=data['reason'],
#             )
#             booking.save()
#             return HttpResponse(booking)
#         else:
#             return HttpResponse("oops!All rooms of this category of rooms are booked.Please try again later.")

# def search_rooms(request):
#     if request.method == 'GET':
#         from_date_str = request.GET.get('from')
#         to_date_str = request.GET.get('to')
#         room_type = request.GET.get('roomType')

#         from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
#         to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

#         booked_rooms = BookingStatus.objects.filter(start_date_lte=to_date, end_date_gte=from_date).values_list('room_no', flat=True)

#         available_rooms = Room.objects.exclude(id__in=booked_rooms).filter(room_type=room_type, status=True)

#         return render(request, 'main.html', {'available_rooms': available_rooms})
#     else:
#         return render(request, 'main.html')

def booking_view(request):
    if request.method == 'POST':
        form = bookingForm(request.POST)
        if form.is_valid():
            # Create a new Request object with the form data
            new_request = Request(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                contact=form.cleaned_data['contact'],
                number_guest=form.cleaned_data['number_guest'],
                reason=form.cleaned_data['reason'],
                check_in=form.cleaned_data['check_in'],
                check_out=form.cleaned_data['check_out']
            )
            new_request.save()
            return redirect('success_page')
    else:
        form = bookingForm()
    
    return render(request, 'availability_form.html', {'form': form})


def success_view(request):
    return render(request, 'success.html')
# def room_view(request):
#     return render(request,)
 


# def send_data(request):
#     data = {'key': 'value'}
#     response = request.post('/admin/Rooms/room', data=data)
# def receive_data(request):
#     key = request.POST.get('key')




# from django.contrib import admin
from django.http import HttpResponse
from .models import Room

class RoomAdmin(admin.ModelAdmin):

    list_display = ("room_no", "location", "status")
    list_filter = ("is_available", "room_type")

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            # path('room/', self.room_view, name='room_view'),  # Modify this line
            path('room/', self.room_redirect, name='room_redirect'),
        ]
        return custom_urls + urls

    def room_redirect(self, request):
        email = request.POST.get('email')
        print(email)
        
        return redirect('/admin/Rooms/room')
        
       
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['heading'] = "Room Information"  # Add your heading here
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(Room, RoomAdmin)
from django.http import JsonResponse
from datetime import datetime



from django.http import JsonResponse
from datetime import datetime
from .models import Room

def available_rooms_view(request):
    req=Request.objects.all()
    check_in_date = request.GET.get('check_in')
    check_out_date = request.GET.get('check_out')

    # Debugging statements
    print(f"Check-in Date: {check_in_date}")
    print(f"Check-out Date: {check_out_date}")

    if check_in_date is None and check_out_date is None:
        return JsonResponse({"error": "Missing check-in or check-out date"}, status=400)

    # Convert strings to datetime objects
    try:
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)

    available_rooms = get_available_rooms(check_in, check_out)
    return JsonResponse(available_rooms, safe=False)

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


# views.py

def print_rooms_view(request):
    rooms = Room.objects.all()
    room_details = [
        f'Room No: {room.room_no}, Location: {room.location}, '
        f'Type: {room.room_type}, Available: {room.is_available}'
        for room in rooms
    ]
    return HttpResponse('<br>'.join(room_details))