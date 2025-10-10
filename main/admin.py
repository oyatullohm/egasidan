from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['email', 'phone', 'first_name', 'last_name', 'is_staff']
#     list_filter = ['is_staff', 'is_superuser', 'is_active']
#     fieldsets = (
#         (None, {'fields': ('email', 'phone', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'phone', 'first_name', 'last_name', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email', 'phone', 'first_name', 'last_name')
#     ordering = ('email',)  # ✅ 'username' emas, 'email' bo'yicha tartiblash
#     filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(CustomUser)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(FCMToken)