"""
URL configuration for Booking project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BookStatus import views
# from Request import views
from BookStatus.views import print_rooms_view, available_rooms_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', views.booking_view, name='booking_view'),
    path('success/', views.success_view, name='success_page'),  # Define a success view to handle post-submission
    path('available_rooms/', available_rooms_view, name='available_rooms'),
    path('signup/', views.signup,name="signup"),
    path('print_rooms/', print_rooms_view, name='print_rooms'),
    path('login/', views.login,name="login"), 
    path('roomlist/', views.RoomList.as_view(),name="RoomList"),
    path('bookinglist/', views.BookingList.as_view(),name="BookingList"),
    # path('requests/', views.request_list, name='request_list'),

    # path('book/',views.BookingView.as_view(),name="BookingView"),
    # path('booking/', views.booking),
    # path('bookingform', views.save_bookingform,name="bookingform"),
    path('', views.main,name="main"),
]