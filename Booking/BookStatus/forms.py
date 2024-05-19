# from django import forms


# class bookingForm(forms.Form):
  
   
#     first_name=forms.CharField()
#     last_name=forms.CharField()
#     email=forms.EmailField()
#     contact=forms.CharField()
#     number_guest=forms.IntegerField()
#     reason=forms.CharField()
#     check_in=forms.DateField()
#     check_out=forms.DateField()



from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

class bookingForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    contact = forms.CharField()
    number_guest = forms.IntegerField(min_value=1)  # Assuming at least one guest
    reason = forms.CharField()
    check_in = forms.DateField()
    check_out = forms.DateField()

    def clean_check_out(self):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')

        if check_in and check_out and check_out <= check_in:
            raise ValidationError(_("Check-out date must be after the check-in date"))
        
        # Check if the booking is for at least one day
        if check_in and check_out and (check_out - check_in).days < 1:
            raise ValidationError(_("Booking must be for at least one day"))

        return check_out

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        # Check if check-in and check-out dates are not in the past
        today = datetime.date.today()
        if check_in and check_in < today:
            raise ValidationError(_("Check-in date cannot be in the past"))
        if check_out and check_out < today:
            raise ValidationError(_("Check-out date cannot be in the past"))

        return cleaned_data


    