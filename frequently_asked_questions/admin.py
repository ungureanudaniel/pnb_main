from django.contrib import admin
from .models import FAQ

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_ro','question_de','created_at', 'updated_at')  # Columns to display in the admin list view
    fields = ['question_en', 'question_ro','question_de', 'answer_en', 'answer_ro', 'answer_de']
    search_fields = ('question', 'answer')  # Fields to include in the admin search

admin.site.register(FAQ, FAQAdmin)
