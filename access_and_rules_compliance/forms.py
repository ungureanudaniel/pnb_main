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
    
    # Override date fields with custom widgets that accept multiple formats
    start_date = forms.DateField(
        label=_('Start Date'),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y']
    )
    end_date = forms.DateField(
        label=_('End Date'),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y']
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
        for field_name, field in self.fields.items():
            if hasattr(field, 'widget') and field_name not in ['start_date', 'end_date']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Make description and area optional
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