from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('api/', include('main.urls')),
    
    path('', admin.site.urls),
    path('accounts/', include('allauth.urls')),

]


