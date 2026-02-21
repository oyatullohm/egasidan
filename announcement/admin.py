from django.contrib import admin
from .models import *

admin.site.register(Category)
# admin.site.register(SubCategory)
admin.site.register(Region)
admin.site.register(Product)
admin.site.register(Complaint)
admin.site.register(Image)
admin.site.register(Model)

admin.site.register(Dislike)

