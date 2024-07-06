from email.message import EmailMessage
from django import forms
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, JsonResponse
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
# from BookStatus.functions.availability import get_available_rooms,check_availability    
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import admin
from django.http import HttpResponse
from .models import Room
from Request.models import Request
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from Users.tokens import generate_token
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# requests = Request.objects.all()
# requests.delete()


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
            myuser.is_active=False
            myuser.save()

            # welcome message
            subject= "welcome to guesthouse booking login"
            message="hello "+myuser.first_name + " !! \n"+ "Click on the link to create your account!! "
            from_email= settings.EMAIL_HOST_USER
            to_email=[myuser.email]
            # send_mail(subject,message,from_email,to_email,fail_silently=True)
            
        
            # confirmation mail
            current_site=get_current_site(request)
            confirm_subject= "confirm your email at Guesthouse Booking website"
            confirm_message= render_to_string('account/email_confirmation.html',{
                'name':myuser.first_name,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token':generate_token().make_token(myuser)
            })

            send_mail(confirm_subject,confirm_message,from_email,to_email,fail_silently=True)
            # email=EmailMessage(confirm_subject,confirm_message,from_email,to_email,)
            # email.fail_silently=True
            # email.send()
            return HttpResponse("you are succesfully registered!")
            

    return render(request,'account/signup.html')



def activate(request,uid64,token):
    try: 
        uid=force_str(urlsafe_base64_decode(uid64))
        myuser=User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token().check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        auth_login(request,myuser)
        return redirect('main')
    else:
        return render(request,'account/activation_failed.html')
    






def login(request):
    if(request.method=="POST"):
        email=request.POST.get('email')
        pass1=request.POST.get('pass')
        user=authenticate(email=email, password=pass1)
        if user is not None:
            auth_login(request,user)
            fname=user.first_name
            return render(request,'main.html',{'user':user})
        else:
            messages.error(request,"invalid credentials")
            return redirect('login')


    return render(request,'account/login.html')


def faq_view(request):
    return render(request, 'faq.html')


@login_required
def main(request):
    user_name = f"{request.User.first_name} {request.User.last_name}"
    return render(request, 'main.html', {'user_name': user_name})

def main(request):
    return render(request, 'main.html')


def logout_view(request):
    logout(request)
    return redirect('main')
# views.py
@login_required
def profile(request):
    # Fetch the user details
    user = request.user
    
    # Fetch booking status for the user
    bookings = BookingStatus.objects.filter(booked_by=f"{user.first_name} {user.last_name}")

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'bookings': bookings,
    }
    
    return render(request, 'view_profile.html', context)





# Create your views here.
class RoomAdmin(admin.ModelAdmin):
    
    list_display = ("room_no", "location")
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
        print("hii")
        print(email)
        
        return redirect('/admin/Rooms/room')
        
       
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['heading'] = "Room Information"  # Add your heading here
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(Room, RoomAdmin)



@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    print("hello")
    change_list_template = 'templates/request_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        requests_all = Request.objects.all()
        
        # Prepare data for each request
        request_data = []
        available_rooms = Room.objects.all()
        
        for r in requests_all:
            available=r.get_available_rooms()
            
            # print(r)
            # print(available)
            request_data.append({
                'request': r,
                'available_rooms': available,
    
            })
            # print(available_rooms,r.first_name,r.last_name)
       
        
        extra_context['request_data'] = request_data
        return super().changelist_view(request, extra_context=extra_context)
    

@login_required
def booking_view(request):
    if not request.user.first_name or not request.user.last_name:
        return redirect('signup')  # Redirect to the signup page if user details are incomplete
    
    if request.method == 'POST':
        form = bookingForm(request.POST)
        if form.is_valid():
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
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = bookingForm(initial=initial_data)
    
    return render(request, 'Booking_form.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')



def assign_room(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        id = request.POST.get('id')
        room_no = request.POST.get('room_no')
        action = request.POST.get('action')

        try:
            request_obj = Request.objects.get(id=id)

            if action == 'delete_request':
                request_obj.delete()
                return JsonResponse({'success': True, 'action': action})

            if action == 'send_email':
                
                room = Room.objects.get(room_no=room_no)
                booking = BookingStatus.objects.create(
                    room_no=room,
                    start_date=request_obj.check_in,
                    end_date=request_obj.check_out,
                    booked_by=f"{request_obj.first_name} {request_obj.last_name}",
                    is_accepted=True,
                )
                booking.save()
                
                # Prepare booking confirmation email
                subject = "Booking Confirmation - Guesthouse Booking"
                message = render_to_string('account/booking_confirmation.html', {
                    'first_name': request_obj.first_name,
                    'last_name': request_obj.last_name,
                    'room_no': room.room_no,
                    'room_type': room.room_type,
                    'room_location': room.location,
                    'check_in': request_obj.check_in,
                    'check_out': request_obj.check_out,
                })
                plain_message = strip_tags(message)
                from_email = settings.EMAIL_HOST_USER
                to_email = [email]

                send_mail(subject, plain_message, from_email, to_email, fail_silently=True, html_message=message)

                # Update the status of the request
                request_obj.status = 'Accepted'
                request_obj.save()

                return JsonResponse({'success': True, 'action': action})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


