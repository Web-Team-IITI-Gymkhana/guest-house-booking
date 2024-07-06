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
from django.contrib.auth import views as auth_views
# from Request import views
# from BookStatus.views import print_rooms_view, available_rooms_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', views.booking_view, name='booking_view'),
    path('success/', views.success_view, name='success_page'), 
    path('accounts/signup/', views.signup,name="signup"),
    path('accounts/login/', views.login,name="login"), 
    path('accounts/logout/', views.logout_view, name='logout'),
    path('activate/<uid64>/<token>', views.activate,name="activate"), 
    path('', views.main,name="main"),
    path('profile/', views.profile, name='profile'),
    path('faq/', views.faq_view, name='faq'),
    path('assign-room/', views.assign_room, name='assign-room'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),
    
   
    
]