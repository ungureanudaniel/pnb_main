from django.contrib import admin
from services.models import AllowedVehicles, VehicleCategory, AccessArea
from .models import Law, LawCategory
from django import forms

class VehicleCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ['title', 'title_ro', 'title_de','slug',]
    # readonly_fields = ["slug", "slug_ro", 'slug_de']
    prepopulated_fields = {"slug": ("title",),}

class AccessAreaAdmin(admin.ModelAdmin):
    fields = ['name',]
    list_display = ('name',)
#=========overriding the admin form for allowed vehicles in order to strip spaces in car nr input ====
class AllowedVehiclesForm(forms.ModelForm):
    class Meta:
        model = AllowedVehicles
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identification_nr'].widget.attrs['oninput'] = 'this.value = this.value.replace(" ", "");'
        self.fields['identification_nr'].widget.attrs['style'] = 'text-transform: uppercase;'

    def clean_identification_nr(self):
        identification_nr = self.cleaned_data['identification_nr']
        # Strip spaces and capitalize the input
        return identification_nr.strip().upper()

class AllowedVehiclesAdmin(admin.ModelAdmin):
    list_display = ('id', 'identification_nr', 'owner','categ', 'permit_nr', 'timestamp', 'start_date', 'end_date')
    fields = ['owner', 'categ', 'identification_nr', 'permit_nr', 'start_date', 'end_date', 'area', 'description']
    form = AllowedVehiclesForm
class LawCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'name_ro','name_de']
    list_display = ('name',)
    # prepopulated_fields = {"name": ("name_en",),}
class LawAdmin(admin.ModelAdmin):
    fields = ['category', 'title', 'text', 'doc_type', 'doc_nr', 'publish_date', 'language', 'link']
    list_display = ('title', 'doc_nr', 'publish_date')

admin.site.register(Law, LawAdmin)
admin.site.register(LawCategory, LawCategoryAdmin)
admin.site.register(VehicleCategory, VehicleCategoryAdmin)
admin.site.register(AccessArea, AccessAreaAdmin)
admin.site.register(AllowedVehicles, AllowedVehiclesAdmin)