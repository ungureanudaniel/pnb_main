from datetime import date

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
    
    # Define fields with defaults
    start_date = forms.DateField(
        label=_('Start Date'),
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label=_('End Date'),
        initial=lambda: date(date.today().year, 12, 31),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = AllowedVehicles
        exclude = ['slug', 'timestamp']
        
        labels = {
            'owner': _('Owner'),
            'categ': _('Category'),
            'identification_nr': _('Identification Number'),
            'permit_nr': _('Permit Number'),
            'description': _('Description'),
            'area': _('Area'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'categ': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap styling to all fields
        for field in self.fields.values():
            if hasattr(field, 'widget'):
                field.widget.attrs.update({'class': 'form-control'})
        
        # Make fields optional
        self.fields['description'].required = False
        self.fields['area'].required = False

class ExcelUploadForm(forms.Form):
    """Form for uploading an Excel file to import allowed vehicles."""
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap styling to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})