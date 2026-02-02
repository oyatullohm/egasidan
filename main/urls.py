from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import TemplateView
# from drf_yasg.views import get_schema_view
# from rest_framework import permissions
from django.urls import path, include
# from drf_yasg import openapi
from main.views import *
from main.viewsets import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'admin-users', AdminUserViewSet, basename='admin-users')
router.register(r'banners', BannerViewSet, basename='banners')
router.register(r'admin-chat-rooms', AdminChatRoomViewSet, basename='admin-chat-rooms')
router.register(r'admin-messages', AdminMessageViewSet, basename='admin-messages')
router.register(r'admin-products', AdminProductViewSet, basename='admin-products')
router.register(r'admin-images', AdminImageViewSet, basename='admin-images')
router.register(r'follow', FollowViewSet, basename='follow')
# router.register(r'users', UserViewSet, basename='users')



urlpatterns = [

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('swagger-ui/', TemplateView.as_view(template_name='swagger_ui.html'), name='swagger-ui'),
    path('product/', include('announcement.urls')),
    # path('auth/social/', include('allauth.socialaccount.urls')),
    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    # path('auth/google/', GoogleLoginAPIView.as_view(), name='google_login_api'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verifay/', Vetifay.as_view(), name='verifay'),
    path('get-user/',get_user, name='get_user'),
    # path('password-update/', password_update, name='password_update'),
    path('user-update/',user_update, name='get_update'),
    
    path('chat/chat-crete/',chat_create, name='chat_crete'),
    path('chat/chat-list/',chat_list, name='chat_list'),
    path('chat/message-create/<int:message_id>/',message_create, name='message_create'),
    path('save-fcm-token/', save_fcm_token, name='save_fcm_token'),
    path('save-fcm-token-/', save_fcm_token_, name='save_fcm_token_'),
    # path('get-firebase-key/', get_firebase_key, name='save_fcm_token_'),
    path('chat/message-list/<int:message_id>/',message_list, name='message_list'),
    path('chat/message-delete/<int:pk>/',message_delete, name='message_delete'),
    path('chat/chat-delete/<int:pk>/',chat_delete, name='chat_delete'),
    
    path('user-all-user/',all_user, name='all_user'),
    path('user-is-staff/<int:pk>/',user_is_staff, name='user_is_staff'),
    path('user-is-active/<int:pk>/',user_is_active, name='user_is_active'),
    path('user-detail/<int:pk>/',user_detail, name='user_is_detail'),
]
urlpatterns += router.urls