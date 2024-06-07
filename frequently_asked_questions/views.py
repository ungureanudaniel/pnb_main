from django.shortcuts import render
from .models import FAQ

def faq_list(request):
    faqs = FAQ.objects.all()  # Retrieve all FAQ entries from the database
    context = {
        'faqs': faqs  # Context dictionary to pass to the template
    }
    return render(request, 'faqs/faqs.html', context)
