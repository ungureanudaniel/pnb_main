from django import forms
from .models import Testimonial, AttractionCategory, Attraction, Contact,\
Comment, PublicDocsDownloaderEntity
# from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
  
  
class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = _("Your name")
        self.fields['text'].label = _("Write your opinion here")
        self.fields['text'].widget.attrs.update({'class': 'comm_text'})
        self.fields['name'].widget.attrs.update({'class': 'comm_name'})
        self.fields['thumbnail'].label = _("Add a photo of yourself")
        self.fields['thumbnail'].widget.attrs.update({'class': 'comm_img'})
        self.fields['name'].widget.attrs['style'] = "width:500px"
        self.fields['thumbnail'].widget.attrs['style'] = "width:500px"
        self.fields['text'].widget.attrs['style'] = "width:500px"
    class Meta:
        model=Comment
        fields=['name', 'text', 'thumbnail']
#----------file download form-----------
class CouncilDocsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CouncilDocsForm, self).__init__(*args, **kwargs)
        self.fields['institution'].label = _("Numele instituției dvs.")
        self.fields['name'].label = _("Numele dvs.")
        self.fields['email'].label = _("Adresa dvs. de email")

        self.fields['institution'].widget.attrs['style']="width:450px;margin:0 20px 20px 0px;"
        self.fields['name'].widget.attrs['style']="width:450px;margin:0 20px 20px 0px;"
        self.fields['email'].widget.attrs['style']="width:450px;margin:0 20px 20px 0px;"
    class Meta:
        model=PublicDocsDownloaderEntity
        fields=['institution', 'name', 'email']
# attr_choices = AttractionCategory.objects.all().values_list('name', 'name')
#
# attr_choices_list = []
#
# for item in attr_choices:
#     attr_choices_list.append(item)

# class AttractionForm(forms.ModelForm):
#     class Meta:
#         model = Attraction
#         fields = '__all__'
#         # fields = ['name', 'image', 'text', 'categ', 'slug']
#         # exclude = ('slug',)
#         widgets = {
#             'name': forms.TextInput(attrs = {'class': 'form-control',}),
#             'text': forms.TextInput(attrs = {'class': 'form-control'}),
#             'categ': forms.Select(choices=attr_choices_list, attrs = {'class': 'form-control'}),
#         }
#
#
# class GalleryForm(forms.ModelForm):
#     class Meta:
#         model = Gallery
#         fields = '__all__'
#         # fields = ['name', 'image', 'text', 'categ', 'slug']
#         # exclude = ('slug',)
#         widgets = {
#             'name': forms.TextInput(attrs = {'class': 'form-control'}),
#             'text': forms.TextInput(attrs = {'class': 'form-control'}),
#             'categ': forms.Select(choices=attr_choices_list, attrs = {'class': 'form-control'}),
#         }

class TestimonialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestimonialForm, self).__init__(*args, **kwargs)
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
class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['author', 'email', 'phone', 'subject', 'text']
        widgets = {
            'author': forms.TextInput(attrs = {'class': 'form__field', 'placeholder': _('Full name...')}),
            'email': forms.EmailInput(attrs = {'class': 'form__field', 'placeholder': 'Email...'}),
            'phone': forms.TextInput(attrs = {'class': 'form__field', 'placeholder': _('Phone number...')}),
            'subject': forms.TextInput(attrs= {'class': 'form__field', 'placeholder': _('Subject...')}),
            'text': forms.TextInput(attrs= {'class': 'form__field form__message', 'placeholder': _('Your message...')}),


        }
