from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _


class CaptchaForm(forms.Form):
    captcha = CaptchaField()

#==========user personal information for payment================
class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['fname'].label = _("Your first name")
        self.fields['lname'].label = _("Your last name")
        self.fields['text'].label = _("Tell us about your experience here")
        self.fields['email'].label = _("Write your email in here")

        self.fields['fname'].widget.attrs['style'] = "width:450px;margin:0 20px 20px 0px;"
        self.fields['lname'].widget.attrs['style'] = "width:450px;margin:0 20px 20px 0px;"
        self.fields['thumbnail'].widget.attrs['style'] = "margin: 0 20px 20px 0px;"
        self.fields['email'].widget.attrs['style'] = "width:450px;margin-bottom:10px;"
        self.fields['text'].widget.attrs['style'] = "margin-left: 0;width:450px;height:300px"
        # self.fields['text'].widget.attrs['style'] = ""
    class Meta:
        model = Testimonial
        fields = ['fname', 'lname', 'email', 'thumbnail', 'text']
        widgets = {
            'fname': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'First name...'}),
            'lname': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Last name...'}),
            'text': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Your experience...'}),
            'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': 'Your email...'}),


        }
