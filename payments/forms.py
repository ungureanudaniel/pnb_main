from django import forms
from .models import *
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
# from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _

# from django_recaptcha.fields import ReCaptchaField
from hcaptcha.fields import hCaptchaField
  
class CaptchaForm(forms.Form):
    hcaptcha = hCaptchaField()
# # class CaptchaForm(forms.Form):
# #     captcha = CaptchaField()

#==========user personal information for payment================
class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['style'] = "width:79px;font-weight:700;margin:15px 10px 20px 0px;border:none"
        self.fields['quantity'].widget.attrs['style'] = "width:40px;margin:0 10px 0px 10px;background-color:#e9ecef"
        # self.fields['quantity_kids'].widget.attrs['style'] = "width:40px;margin:0 10px 0px 10px;background-color:#e9ecef"
        self.fields['currency'].widget.attrs['style'] = "width:320px;margin:0 20px 20px 0px;"
        self.fields['buyer_fname'].widget.attrs['style'] = "width:320px;margin:0 20px 20px 0px;"
        self.fields['buyer_lname'].widget.attrs['style'] = "width:320px;margin:0 20px 20px 0px;"
        self.fields['phone'].widget.attrs['style'] = "margin-bottom: 20px;"
        # self.fields['address'].widget.attrs['style'] = "margin-bottom: 20px;"
        # self.fields['county'].widget.attrs['style'] = "width:320px;margin:0 20px 20px 0px;"
        # self.fields['country'].widget.attrs['style'] = "width:320px;margin:0 20px 20px 0px;"
        # self.fields['city'].widget.attrs['style'] = "width:320px;margin:0 20px 20px 0px;"
        # self.fields['zip'].widget.attrs['style'] = "width:320px;margin:0px 20px 20px 0px;"
        self.fields['notes'].widget.attrs['style'] = "margin-left: 0;width:450px;height:300px"
        self.fields['email'].widget.attrs['style'] = "width:320px;margin-bottom:20px;"

        # Set min and max values for quantity field
        self.fields['quantity'].widget.attrs['max'] = '20' 
        self.fields['quantity'].widget.attrs['min'] = '1'

    def clean_quantity(self):
        """Validate that quantity does not exceed 20 tickets"""
        quantity = self.cleaned_data.get('quantity')

        if quantity and quantity > 20:
            raise forms.ValidationError(_("You cannot purchase more than 20 tickets at once. Please reduce your quantity or contact us for bulk orders."))
        return quantity
    class Meta:
        model = Payment
        fields = ['quantity', 'price', 'currency', 'buyer_fname', 'buyer_lname', 'address', 'county', 'country', 'city', 'zip', 'phone', 'email', 'terms', 'notes']
        exclude = () 
        readonly_fields = ('price',)
        widgets = {
            'quantity': forms.TextInput(attrs = {'class': 'form-control cart-item__input text-center', 'id':'quantity', 'type': 'number', 'name':'adults', 'placeholder': '',}),
            'price': forms.TextInput(attrs = {'class': 'form-control', 'id':'total_price', 'name':'price', 'placeholder': '', 'readonly': 'readonly'}),
            'currency': forms.Select(attrs = {'class': 'form-control', 'placeholder': 'Currency of choice...'}),
            'buyer_fname': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': _("First Name...")}),
            'buyer_lname': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': _("Last Name...")}),
            # 'address': forms.TextInput(attrs = {'class': 'form-control buyer_address', 'placeholder': 'Your street number, building and apartment...'}),
            # 'county': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Your County...'}),
            # 'country': CountrySelectWidget(attrs = {'class': 'form-control', }),
            # 'city': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Your City...'}),
            # 'zip': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Your address ZIP code...'}),
            'phone': forms.TextInput(attrs = {'class': 'form-control buyer_phone', 'placeholder': _("Your phone number (optional)...")}),
            'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': _("Your email...")}),
            'notes': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': _("Additional information if needed...")}),
            'terms': forms.CheckboxInput(attrs = {'class': 'form-control', 'required':'required',})

        }
