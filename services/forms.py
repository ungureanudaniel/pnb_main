from django import forms
from .models import Testimonial, AttractionCategory, Attraction, Contact,\
Gallery, Comment
from ckeditor.widgets import CKEditorWidget
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _


class CaptchaForm(forms.Form):
    captcha = CaptchaField()

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
    class Meta:
        model = Testimonial
        fields = ['fname', 'lname', 'email', 'thumbnail', 'text']
        widgets = {
            'fname': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'First name...'}),
            'lname': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Last name...'}),
            # 'email': forms.EmailInput(),


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
