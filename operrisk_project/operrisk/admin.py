from django.contrib import admin
from operrisk.models import Category, Incident

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'URL_name':('name',)}

# Register your models here.
#admin.site.register(Category)
admin.site.register(Incident)
admin.site.register(Category,CategoryAdmin)

