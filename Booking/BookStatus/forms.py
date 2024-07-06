from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

class bookingForm(forms.Form):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField()
    email = forms.EmailField(required=True)
    contact = forms.CharField(required=True)
    number_guest = forms.IntegerField(min_value=1, required=True) 
    reason = forms.CharField(max_length=40)
    check_in = forms.DateField(required=True)
    check_out = forms.DateField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        today = datetime.date.today()
        if check_in and check_in < today:
            self.add_error('check_in', _("Check-in date cannot be in the past"))
        if check_out and check_out < today:
            self.add_error('check_out', _("Check-out date cannot be in the past"))

        return cleaned_data

    def clean_check_out(self):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')

        if check_in and check_out:
            if check_out <= check_in:
                raise ValidationError(_("Check-out date must be after the check-in date"))

            if (check_out - check_in).days < 1:
                raise ValidationError(_("Booking must be for at least one day"))

        return check_out

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if len(contact) != 10 or not contact.isdigit():
            raise forms.ValidationError("Contact number must be exactly 10 digits long.")
        return contact

    def clean_number_guest(self):
        number_guest = self.cleaned_data['number_guest']
        if number_guest <= 0:
            raise forms.ValidationError("Number of guests must be greater than 0.")
        return number_guest