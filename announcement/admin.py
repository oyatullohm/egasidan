from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Image)
admin.site.register(Brand)
admin.site.register(Modell)
admin.site.register(Vehicle)
admin.site.register(Favorite)
admin.site.register(Dislike)
admin.site.register(Pet)
admin.site.register(Job)
@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_label', 'model')
    search_fields = ('app_label', 'model')
