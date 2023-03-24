from modeltranslation.translator import translator, TranslationOptions
from .models import Team, AttractionCategory, PublicCategory, Attraction,\
BlogPostCategory, BlogPost, Event


class AttractionCatTranslationOptions(TranslationOptions):
    fields = ('name',)

class TeamTranslationOptions(TranslationOptions):
    fields = ('text', 'job')
class PublicCategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)
class AttractionTranslationOptions(TranslationOptions):
    fields = ('name', 'text')
class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'text')
class BlogPostCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)
class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)

translator.register(BlogPost, BlogPostTranslationOptions)
translator.register(BlogPostCategory, BlogPostCategoryTranslationOptions)
translator.register(AttractionCategory, AttractionCatTranslationOptions)
translator.register(Attraction, AttractionTranslationOptions)
translator.register(Event, EventTranslationOptions)
translator.register(Team, TeamTranslationOptions)
translator.register(PublicCategory, PublicCategoryTranslationOptions)
