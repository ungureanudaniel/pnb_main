from django import forms
from .models import Law, LawCategory
# from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField