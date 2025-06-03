from django import forms
from .models import Law, LawCategory
# from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
from services.models import AllowedVehicles


class VehicleForm(forms.ModelForm):
    """Form for creating or updating allowed vehicles."""
    class Meta:
        model = AllowedVehicles
        # Exclude 'slug' and 'timestamp' from the form
        exclude = ['slug', 'timestamp']

        labels = {
            'owner': _('Owner'),
            'categ': _('Category'),
            'identification_nr': _('Identification Number'),
            'permit_nr': _('Permit Number'),
            'start_date': _('Start Date'),
            'end_date': _('End Date'),
            'description': _('Description'),
            'area': _('Area'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap styling to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



class ExcelUploadForm(forms.Form):
    """Form for uploading an Excel file to import allowed vehicles."""
    file = forms.FileField()