from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import *
class CustomRegisterSerializer(RegisterSerializer):
    username = None  # ✅ Usernameni butunlay olib tashlaymiz

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
          
        }
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','phone','first_name','last_name','is_staff','is_active']
    
class MessageSerializer(serializers.ModelSerializer):
    i = serializers.SerializerMethodField()
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'i', 'sender', 'room', 'image', 'content', 'timestamp', ]
    
    def get_i(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.sender.id == request.user.id
        return False
    
class ChatRoomSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    class Meta:
        model = ChatRoom
        fields = ['id','user', 'user_1','user_2','owner','last_message', 'user_2', 'room_name', 'created_at']
    
    def get_user(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if request.user.id != obj.user_1.id:
                return UserSerializer(obj.user_1).data
            return UserSerializer(obj.user_2).data
        return None
    
    def get_last_message(self,obj):
        message =  obj.messages.order_by("-timestamp").first()
        if message:
            return MessageSerializer(message).data
        return None
    
# class DeviceTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DeviceToken
#         fields = ['token']