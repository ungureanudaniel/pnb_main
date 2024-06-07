from modeltranslation.translator import translator, TranslationOptions
from .models import FAQ


class FAQCatTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')

translator.register(FAQ, FAQCatTranslationOptions)