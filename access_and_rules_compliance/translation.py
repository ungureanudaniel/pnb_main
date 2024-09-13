from modeltranslation.translator import translator, TranslationOptions
from .models import LawCategory


class LawCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(LawCategory, LawCategoryTranslationOptions)
