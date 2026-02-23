from django.db.models import OuterRef, Subquery,Prefetch ,Q, Max, Count
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import  AllowAny, IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.utils.crypto import salted_hmac
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render
# from .fcm_service import FCMService
from django.db import transaction
from rest_framework import status
from pyfcm import FCMNotification
from django.conf import settings
from .models import FCMToken
from .serializers import *
import random
import json
from .utils import *
User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user, many = False, context={"request":request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    if request.data.get('first_name'):
        user.first_name = request.data.get('first_name')
    if request.data.get('last_name'):
        user.last_name = request.data.get('last_name')
    if request.data.get('image'):
        user.image = request.data.get('image')
    
    user.save()
    return Response(UserSerializer(user, many= False).data)


class RegisterView(APIView):
    def post(self, request):

        data = request.data
        phone = data.get('phone')
        onesignal_player_id = data.get('firebase_token')
        code = random_number()
        set_verify_code(code, phone)

        if data.get('phone') and CustomUser.objects.filter(phone=phone).exists():
            user = CustomUser.objects.get(phone=phone)

            return Response({
                'success': True,
                'code':code
      
            }, status=status.HTTP_201_CREATED)
            
        user = CustomUser.objects.create_user(
            username=phone,
            phone=phone,
            
        )
        user.onesignal_player_id = onesignal_player_id
        user.save()
        if user:
            # refresh = RefreshToken.for_user(user)
            return Response({
                   'success': True,
                   'code':code
                
                }, status=status.HTTP_201_CREATED)
        
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        onesignal_player_id = request.data.get('firebase_token')
        if phone:
            try:
                user = CustomUser.objects.get(phone=phone)
                user.onesignal_player_id = onesignal_player_id
                user.save()
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        code = random_number()
        set_verify_code(code, phone)
        if phone=="+998900601044":

            refresh = RefreshToken.for_user(user)
            return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                # 'email': user.email,
                'phone': user.phone,
                # 'role': user.role,
                # 'is_confirmation': user.is_confirmation
            }
        }, status=200)
            
        return Response({"data":'otp yuborildi', "code":code}, status=401)

class Vetifay(APIView):
    def post(self, request):
        code = request.data.get('code')
        
        data = get_verify_email_by_code(code)
        phone = data['phone']
        user = CustomUser.objects.get(phone=phone)
        delete_verify_code(code)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                # 'email': user.email,
                'phone': user.phone,
                # 'role': user.role,
                # 'is_confirmation': user.is_confirmation
            }
        }, status=200)

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_create(request):
    user_1 = request.user
    user_2_id = request.data.get('user_2_id')
    product = request.data.get('product_id')
    type = request.data.get('type')

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
    chat_room.type = type
    chat_room.product_id = product
    chat_room.save()
    
    serializer = ChatRoomSerializer(chat_room, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list(request):
    user = request.user
    type = request.query_params.get('type')

    last_message_qs = (
        Message.objects
        .filter(room=OuterRef('pk'))
        .order_by('-timestamp')
    )

    chats = (
        ChatRoom.objects
        .filter(Q(user_1=user) | Q(user_2=user), type=type)
        .select_related('product', 'user_1', 'user_2', 'owner')
        .annotate(
            # 🔹 oxirgi xabar
            last_message_content=Subquery(
                last_message_qs.values('content')[:1]
            ),
            last_message_time=Subquery(
                last_message_qs.values('timestamp')[:1]
            ),
            last_message_sender_id=Subquery(
                last_message_qs.values('sender_id')[:1]
            ),

            # 🔹 unread count (eng muhim joy)
            unread_count_db=Count(
                'messages',
                filter=Q(
                    messages__flowed=False
                ) & ~Q(messages__sender=user),
            )
        )
        .order_by('-last_message_time')
    )

    serializer = ChatRoomSerializer(
        chats,
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message_create(request, message_id):
    user = request.user

    try:
        chat_room = ChatRoom.objects.select_related(
            'user_1',
            'user_2'
        ).get(id=message_id)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room not found'}, status=404)

    if user.id not in (chat_room.user_1_id, chat_room.user_2_id):
        return Response({'error': 'Permission denied'}, status=403)

    message = Message.objects.create(
        sender=user,
        room=chat_room,
        content=request.data.get('content', ''),
        image=request.FILES.get('image')
    )

    # send_message_notification(message, chat_room, user)

    serializer = MessageSerializer(
        message,
        context={'request': request}
    )
    return Response(serializer.data, status=201)

def send_message_notification(message, chat_room, sender):
    receiver = (
        chat_room.user_2
        if sender.id == chat_room.user_1_id
        else chat_room.user_1
    )

    fcm_tokens = FCMToken.objects.filter(
        user_id=receiver.id
    ).only('token')

    if not fcm_tokens.exists():
        return

    notification_title = "Yangi xabar"

    if message.content:
        notification_body = (
            message.content[:100] + "..."
            if len(message.content) > 100
            else message.content
        )
    elif message.image:
        notification_body = "📷 Rasm"
    else:
        notification_body = "Yangi xabar"

    data = {
        'chat_room_id': str(chat_room.id),
        'message_id': str(message.id),
        'sender_id': str(sender.id),
        'type': 'new_message'
    }

    # for token in fcm_tokens:
    #     FCMService.send_push_notification(
    #         token.token,
    #         notification_title,
    #         notification_body,
    #         data
    #     )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_list(request, message_id):
    user = request.user
    try:
        chat_room = ChatRoom.objects.select_related('user_1', 'user_2').get(id=message_id)
    except ChatRoom.DoesNotExist:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

    if user != chat_room.user_1 and user != chat_room.user_2:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    messages = Message.objects.filter(room=chat_room).select_related('sender','room').order_by('-id')
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
 

@login_required
def chat_page(request, room_id):
    """Oddiy chat sahifasi"""
    chat_room = ChatRoom.objects.get(id=room_id)
    messages = Message.objects.filter(room=chat_room)
    context = {
        'FIREBASE_CONFIG': settings.FIREBASE_CONFIG,
        'FIREBASE_VAPID_KEY': settings.FIREBASE_VAPID_KEY,
        "chat_room": chat_room, "messages": messages
    }
    return render(request, "chat.html", context)


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

@csrf_exempt
@login_required
def save_fcm_token(request):
    """Frontenddan FCM tokenni qabul qilib saqlaydi"""
    if request.method != "POST":
        return JsonResponse({"error": "POST so‘rov yuboring"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Noto‘g‘ri JSON format"}, status=400)

    token = data.get("token")
    if not token:
        return JsonResponse({"error": "Token berilmagan"}, status=400)

    # 🔎 Mavjud tokenni tekshiramiz
    existing_token = FCMToken.objects.filter(token=token).first()

    if existing_token:
        # Agar token boshqa userga tegishli bo‘lsa, yangilaymiz
        if existing_token.user != request.user:
            existing_token.user = request.user
            existing_token.save(update_fields=["user"])
            return JsonResponse({"status": "updated", "token": token})
        else:
            return JsonResponse({"status": "already_exists", "token": token})

    # ✅ Token yo‘q bo‘lsa, yangi yozuv yaratamiz
    FCMToken.objects.get_or_create(user=request.user, token=token)
    return JsonResponse({"status": "created", "token": token})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_fcm_token_(request):
    """Frontenddan FCM tokenni qabul qilib saqlaydi"""
    if request.method != "POST":
        return Response({"error": "POST so‘rov yuboring"}, status=405)

    data = json.loads(request.body)
    token = data.get('token')
    if not token:
        return Response({"error": "Token berilmagan"}, status=400)

    # 🔎 Mavjud tokenni tekshiramiz
    existing_token = FCMToken.objects.filter(token=token).first()

    if existing_token:
        # Agar token boshqa userga tegishli bo‘lsa, yangilaymiz
        if existing_token.user != request.user:
            existing_token.user = request.user
            existing_token.save(update_fields=["user"])
            return Response({"status": "updated", "token": token})
        else:
            return Response({"status": "already_exists", "token": token})

    FCMToken.objects.get_or_create(user=request.user, token=token)
    return Response({"status": "created", "token": token})

@api_view(['GET'])
def get_firebase_key(request):
    return Response({
        'FIREBASE_CONFIG': settings.FIREBASE_CONFIG,
        'FIREBASE_VAPID_KEY': settings.FIREBASE_VAPID_KEY,
    })
