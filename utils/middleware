from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext_lazy as _


class LanguageMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        function to activate the translation
        """
        if 'lang' in request.GET:
            language = request.GET.get('lang', 'id')
            if language in dict(settings.LANGUAGES).keys():
                request.session['_language'] = language

        language = request.session.get('_language', 'id')
        translation.activate(language)