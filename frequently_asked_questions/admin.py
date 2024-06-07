from django.contrib import admin
from .models import FAQ

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'updated_at')  # Columns to display in the admin list view
    search_fields = ('question', 'answer')  # Fields to include in the admin search

admin.site.register(FAQ, FAQAdmin)
