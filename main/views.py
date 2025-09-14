from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.response import Response
from google.auth.transport import requests
from rest_framework.views import APIView
from google.oauth2 import id_token
from rest_framework import status
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
def user_is_staff(request, pk):
    try:
        user = CustomUser.objects.get(id=pk)
    except CustomUser.DoesNotExist:
        return Response({'success': False, 'error': 'User not found'}, status=404)

    if not request.user.is_staff:  # faqat staff foydalanuvchilar o‘zgartira oladi
        return Response({'success': False, 'error': 'Permission denied'}, status=403)

    staff = request.data.get('is_staff')  
    if staff is not None:  
        user.is_staff = bool(int(staff))  
        user.save()

    return Response({'success': True, 'user': UserSerializer(user).data})


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
                    'phone': user.phone
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




        