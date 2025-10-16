from django.contrib import admin
from django.urls import path, include

from main.views import chat_page , send_message_view


urlpatterns = [
    path('chat/<int:room_id>/send/',send_message_view, name='send_message'),
    path('chat/<int:room_id>/', chat_page, name='chat_page'),
    path('api/', include('main.urls')),
    path('', admin.site.urls),
    path('accounts/', include('allauth.urls')),

]


