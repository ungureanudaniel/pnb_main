from modeltranslation.translator import translator, TranslationOptions
from .models import Team, AttractionCategory, PublicCategory, Attraction,\
BlogPostCategory, BlogPost, Event, Announcement, FloraCategory,\
WildlifeCategory, Flora, Wildlife, SCouncil


class AttractionCatTranslationOptions(TranslationOptions):
    fields = ('name',)
class AttractionTranslationOptions(TranslationOptions):
    fields = ('name', 'text',)
class FloraCatTranslationOptions(TranslationOptions):
    fields = ('name',)
class FloraTranslationOptions(TranslationOptions):
    fields = ('name', 'habitat', 'text')
class WildlifeCatTranslationOptions(TranslationOptions):
    fields = ('name',)
class WildlifeTranslationOptions(TranslationOptions):
    fields = ('name', 'habitat', 'text', 'diet')
class TeamTranslationOptions(TranslationOptions):
    fields = ('text', 'job', 'sector')
class PublicCategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)
class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)
class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)
class BlogPostCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)
class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)
class SCouncilTranslationOptions(TranslationOptions):
    fields = ('interest',)
translator.register(BlogPost, BlogPostTranslationOptions)
translator.register(Announcement, AnnouncementTranslationOptions)
translator.register(BlogPostCategory, BlogPostCategoryTranslationOptions)
translator.register(AttractionCategory, AttractionCatTranslationOptions)
translator.register(Attraction, AttractionTranslationOptions)
translator.register(Event, EventTranslationOptions)
translator.register(Team, TeamTranslationOptions)
translator.register(PublicCategory, PublicCategoryTranslationOptions)
translator.register(FloraCategory, FloraCatTranslationOptions)
translator.register(WildlifeCategory, WildlifeCatTranslationOptions)
translator.register(Flora, FloraTranslationOptions)
translator.register(Wildlife, WildlifeTranslationOptions)
translator.register(SCouncil, SCouncilTranslationOptions)
