from django.contrib import admin
from operrisk.models import Category, Incident, Subcategory
from django.contrib.auth.models import Permission

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'URL_name':('name',)}

class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'URL_name':('name',)}

# Register your models here.
admin.site.register(Incident)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Subcategory,SubcategoryAdmin)
admin.site.register(Permission)

