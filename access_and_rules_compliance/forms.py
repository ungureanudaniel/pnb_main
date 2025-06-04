from django import forms
# from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from services.models import AllowedVehicles, VehicleCategory, AccessArea

class VehicleCategoryForm(forms.ModelForm):
    """Form for creating or updating vehicle categories."""
    class Meta:
        model = VehicleCategory
        fields = ['title']

        labels = {
            'title': _('Title'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap styling to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class VehicleAccessAreaForm(forms.ModelForm):
    """Form for creating or updating vehicle access areas."""
    class Meta:
        model = AccessArea
        fields = ['name']

        labels = {
            'name': _('Access Area'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap styling to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap styling to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})