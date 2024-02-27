from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
# from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _

from django_recaptcha.fields import ReCaptchaField
  
  
class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()
# # class CaptchaForm(forms.Form):
# #     captcha = CaptchaField()

#==========user personal information for payment================
class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        # self.fields['price'].label = _("Total amount in selected currency")
        # self.fields['quantity'].label = _("Total number of tickets")
        # self.fields['currency'].label = _("Select desired currency")
        # self.fields['buyer_fname'].label = _("Your first name")
        # self.fields['buyer_lname'].label = _("Your last name")
        # self.fields['address'].label = _("Your address")
        # self.fields['county'].label = _("Your county of residence")
        # self.fields['country'].label = _("Your country of residence")
        # self.fields['city'].label = _("Your city of residence")
        # self.fields['zip'].label = _("Your address zip code")
        # self.fields['phone'].label = _("Your phone number")
        # self.fields['email'].label = _("Your email address")
        # self.fields['notes'].label = _("You can write some notes here")

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
    class Meta:
        model = Payment
        fields = ['quantity', 'price', 'currency', 'buyer_fname', 'buyer_lname', 'address', 'county', 'country', 'city', 'zip', 'phone', 'email', 'terms', 'notes']
        exclude = () 
        readonly_fields = ('price',)
        widgets = {
            'quantity': forms.TextInput(attrs = {'class': 'form-control cart-item__input text-center', 'id':'quantity', 'type': 'number', 'name':'adults', 'placeholder': '',}),
            'price': forms.TextInput(attrs = {'class': 'form-control', 'id':'total_price', 'name':'price', 'placeholder': '', 'readonly': 'readonly'}),
            'currency': forms.Select(attrs = {'class': 'form-control', 'placeholder': 'Currency of choice...'}),
            'buyer_fname': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'First name...'}),
            'buyer_lname': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Last name...'}),
            # 'address': forms.TextInput(attrs = {'class': 'form-control buyer_address', 'placeholder': 'Your street number, building and apartment...'}),
            # 'county': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Your County...'}),
            # 'country': CountrySelectWidget(attrs = {'class': 'form-control', }),
            # 'city': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Your City...'}),
            # 'zip': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Your address ZIP code...'}),
            'phone': forms.TextInput(attrs = {'class': 'form-control buyer_phone', 'placeholder': 'Your phone number (optional)...'}),
            'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': 'Your email...'}),
            'notes': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Additional information if needed...'}),
            'terms': forms.CheckboxInput(attrs = {'class': 'form-control', 'required':'required',})

        }
