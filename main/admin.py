from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(CustomUser)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(FCMToken)
admin.site.register(UserFollow)
admin.site.register(Banner)
