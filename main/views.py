from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.response import Response
from google.auth.transport import requests
from rest_framework.views import APIView
from django.db.models import Max
from google.oauth2 import id_token
from rest_framework import status
from pyfcm import FCMNotification
from django.conf import settings
from .serializers import *
User = get_user_model()

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user, many = False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    user.first_name = request.data['first_name']
    user.last_name = request.data['last_name']
    user.save()
    return Response(UserSerializer(user, many= False).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # faqat login bo'lgan userlarga ruxsat
def password_update( request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    # Eski parolni tekshirish
    if not user.check_password(old_password):
        return Response({"error": "Eski parol noto'g'ri!"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({"success": "Parol muvaffaqiyatli o'zgartirildi!"}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if data.get('email') and User.objects.filter(email=data['email']).exists():
            return Response({'email': 'Bu email allaqachon ro‘yxatdan o‘tgan.'}, status=status.HTTP_400_BAD_REQUEST)
        if data.get('phone') and User.objects.filter(phone=data['phone']).exists():
            return Response({'phone': 'Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomRegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save(request)
            user.phone= data.get('phone')
            # user.is_staff= True
            # user.is_superuser= True
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'phone': user.phone
                }
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': user.phone,
                    "is_staff":user.is_staff
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token is None:
            return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


class GoogleLoginAPIView(APIView):
    def post(self, request):
        token = request.data.get('id_token')

        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.SOCIALACCOUNT_PROVIDERS['google']['APP'][0]['client_id']
            )

    
            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name, 'last_name': last_name}
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })

        except ValueError as e:
            print("Token validatsiyasida xato:", e)  # Xatoni konsolga chiqaradi
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_create(request):
    user_1 = request.user
    user_2_id = request.data.get('user_2_id')

    try:
        user_2 = User.objects.get(id=user_2_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if user_1.id == user_2.id:
        return Response({'error': 'Cannot create chat with yourself'}, status=status.HTTP_400_BAD_REQUEST)

    # ChatRoom nomini yaratish (kichik ID birinchi bo'lishi kerak)
    ids = sorted([user_1.id, user_2.id])
    room_name = f"chat_{ids[0]}_{ids[1]}"

    chat_room, created = ChatRoom.objects.get_or_create(
        user_1__in=[user_1, user_2],
        user_2__in=[user_1, user_2],
        defaults={'user_1': user_1, 'user_2': user_2, 'owner': user_1, 'room_name': room_name}
    )

    serializer = ChatRoomSerializer(chat_room)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    chats = (
        ChatRoom.objects.filter(models.Q(user_1=user) | models.Q(user_2=user))
        .annotate(last_message=Max("messages__timestamp"))  # eng so‘nggi xabar
        .select_related("user_1", "user_2").prefetch_related('messages')
        .order_by("-last_message")  # oxirgi xabar bo‘yicha saralash
    )
    serializer = ChatRoomSerializer(chats, many=True,context={'request': request})
    return Response(serializer.data)

# views.py
from django.db import transaction
from .fcm_service import FCMService
from .models import FCMToken

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message_create(request, message_id):
    user = request.user
    try:
        chat_room = ChatRoom.objects.get(id=message_id)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    if user != chat_room.user_1 and user != chat_room.user_2:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    content = request.data.get('content', '')
    image = request.FILES.get('image', None)

    with transaction.atomic():
        message = Message.objects.create(
            sender=request.user,
            room=chat_room,
        )
        if content:
            message.content = content
        if image:
            message.image = image
        message.save()

        # Push notification yuborish
        send_message_notification(message)

    serializer = MessageSerializer(message, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def send_message_notification(message):
    """Xabar yuborilganda push notification yuborish"""
    sender = message.sender
    chat_room = message.room
    
    # Kimga notification yuborilishi kerak
    if sender == chat_room.user_1:
        receiver = chat_room.user_2
    else:
        receiver = chat_room.user_1
    
    # Qabul qiluvchining FCM token larini olish
    try:
        fcm_tokens = FCMToken.objects.filter(user=receiver)
        
        notification_title = f"Yangi havar"
        notification_body = message.content[:100] + "..." if len(message.content) > 100 else message.content
        
        # Agar content bo'sh bo'lsa va rasm bo'lsa
        if not message.content and message.image:
            notification_body = "📷 Rasm"
        
        data = {
            'chat_room_id': str(chat_room.id),
            'message_id': str(message.id),
            'sender_id': str(sender.id),
            'type': 'new_message'
        }
        
        # Har bir token ga notification yuborish
        for fcm_token in fcm_tokens:
            FCMService.send_push_notification(
                fcm_token.token,
                notification_title,
                notification_body,
                data
            )
            
    except FCMToken.DoesNotExist:
        # FCM token topilmadi
        pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_fcm_token(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Eski token larni o'chirish (optional)
    FCMToken.objects.filter(user=request.user).delete()
    
    # Yangi token ni saqlash
    fcm_token, created = FCMToken.objects.get_or_create(
        user=request.user,
        token=token
    )
    
    return Response({
        'status': 'success',
        'created': created
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_list(request, message_id):
    user = request.user
    try:
        chat_room = ChatRoom.objects.get(id=message_id)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    if user != chat_room.user_1 and user != chat_room.user_2:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    messages = Message.objects.filter(room=chat_room).select_related('sender','room').order_by('timestamp')
    serializer = MessageSerializer(messages, many=True,context={'request': request})
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def message_delete(request, pk):
    user = request.user
    try:
        message = Message.objects.get(id=pk)
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    if message.sender != user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    message.delete()
    return Response({'success': 'Message deleted'}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def chat_delete(request, pk):
    user = request.user
    try:
        chat_room = ChatRoom.objects.get(id=pk)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    if chat_room.owner != user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    message = Message.objects.filter(room=chat_room)
    if message:
        message.delete()
    chat_room.delete()
    return Response({'success': 'Chat room deleted'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_user(request):
    if request.user.is_staff:
        user =CustomUser.objects.all().order_by('-id')
        serializers = UserSerializer(user, many= True)
        return Response(serializers.data)
    return Response({'permission':False})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_is_staff(request,pk):
    if request.user.is_staff:
        try:
            user = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response ({"user": None})
        is_staff = False if user.is_staff else True
        user.is_staff = is_staff
        user.save()
        return Response({'success':is_staff})
    return Response({'permission':None})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_is_active(request,pk):
    if request.user.is_staff:
        try:
            user = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response ({"user": None})
        is_active = False if user.is_active else True
        user.is_active = is_active
        user.save()
        return Response({'success':is_active})
    return Response({'permission':None})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request,pk):
    if request.user.is_staff:
        try:
            user = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response ({"user": None})
        return Response(UserSerializer(user, many=False).data)
    return Response({'permission':None})
 
   
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

@login_required
def chat_page(request, room_id):
    """Oddiy chat sahifasi"""
    chat_room = ChatRoom.objects.get(id=room_id)
    messages = Message.objects.filter(room=chat_room)
    return render(request, "chat.html", {"chat_room": chat_room, "messages": messages})


@login_required
def send_message_view(request, room_id):
    """Ajax orqali xabar yuborish"""
    if request.method == "POST":
        content = request.POST.get("content", "")
        image = request.FILES.get("image")

        try:
            chat_room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return JsonResponse({"error": "Chat topilmadi"}, status=404)

        with transaction.atomic():
            message = Message.objects.create(
                sender=request.user,
                room=chat_room,
                content=content
            )
            if image:
                message.image = image
            message.save()

            # Push notification yuborish
            send_message_notification(message)

        return JsonResponse({
            "id": message.id,
            "sender": message.sender.id,
            "content": message.content,
        })

    return JsonResponse({"error": "Noto‘g‘ri so‘rov"}, status=400)



# push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)

# class RegisterDevice(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         token = request.data.get('token')
#         DeviceToken.objects.update_or_create(user=request.user, defaults={'token': token})
#         return Response({"message": "Token saqlandi"})

# class SendNotification(APIView):
#     def post(self, request):
#         title = request.data.get('title')
#         body = request.data.get('body')
#         tokens = list(DeviceToken.objects.values_list('token', flat=True))
#         result = push_service.notify_multiple_devices(
#             registration_ids=tokens,
#             message_title=title,
#             message_body=body
#         )
#         return Response(result)               
        
    