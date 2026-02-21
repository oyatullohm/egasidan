from django.contrib import admin
from django.urls import path, include
from django.http import FileResponse
from django.conf import settings
from django.conf.urls.static import static
import os
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def firebase_sw(request):
    file_path = os.path.join(settings.BASE_DIR, 'static', 'firebase-messaging-sw.js')
    return FileResponse(open(file_path, 'rb'), content_type='application/javascript')

from main.views import chat_page , send_message_view, save_fcm_token



urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Brauzerda sinash uchun Swagger interfeysi
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('firebase-messaging-sw.js', firebase_sw, name='firebase_sw'),
    path('chat/<int:room_id>/send/',send_message_view, name='send_message'),
    path('chat/<int:room_id>/', chat_page, name='chat_page'),
     path('save-token/', save_fcm_token, name='save_fcm_token'),
    path('api/', include('main.urls')),
    path('', admin.site.urls),
    # path('accounts/', include('allauth.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



