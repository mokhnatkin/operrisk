from django.contrib import admin
from operrisk.models import Category, Incident
from django.contrib.auth.models import Permission

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'URL_name':('name',)}

# Register your models here.
admin.site.register(Incident)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Permission)

