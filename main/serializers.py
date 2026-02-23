# from dj_rest_auth.registration.serializers import RegisterSerializer
from announcement.models import Product, Image
from rest_framework import serializers
from .models import *
from django.db.models import Q
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','phone','image','first_name','last_name','is_staff','is_active']
    
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

class ProductShortSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'image']

    def get_image(self, obj):
        
        if obj.image.exists():
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image[0].url)
        return None
from announcement.models import Product
class ProductShortSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField() 
    class Meta:
        model = Product
        fields = ['id', 'title', 'price','money_type','image']
        

    def get_image(self, obj):
        images = getattr(obj, 'prefetched_images', [])
        if images:
            request = self.context.get('request')
            return request.build_absolute_uri(images[0].image.url)
        return None

class ChatRoomSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.IntegerField(source='unread_count_db', read_only=True)
    product = ProductShortSerializer(read_only=True)
    class Meta:
        model = ChatRoom
        fields = [
            'id',
            'product',
            'user',
            'user_1',
            'user_2',
            'owner',
            'type',
            'last_message',
            'room_name',
            'created_at',
            'unread_count'
        ]

    def get_user(self, obj):
        request = self.context.get('request')
        if request.user.id == obj.user_1.id:
            return UserSerializer(obj.user_2, context=self.context).data
        return UserSerializer(obj.user_1, context=self.context).data

    def get_last_message(self, obj):
        # Agar annotate orqali kelgan bo‘lsa
        if hasattr(obj, 'last_message_time'):
            if not obj.last_message_time:
                return None
            return {
                'content': obj.last_message_content,
                'timestamp': obj.last_message_time,
                'sender_id': obj.last_message_sender_id,
            }

        # Agar annotate YO‘Q bo‘lsa (masalan chat_create)
        last_message = obj.messages.order_by('-timestamp').first()
        if not last_message:
            return None

        return {
            'content': last_message.content,
            'timestamp': last_message.timestamp,
            'sender_id': last_message.sender_id,
        }




class FollowingSerializer(serializers.ModelSerializer):
    following = UserSerializer(read_only=True)  # kimga obuna bo‘lganman

    class Meta:
        model = UserFollow
        fields = ['id', 'following', 'follower','created_at']



class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)  # menga kim obuna bo‘lgan

    class Meta:
        model = UserFollow
        fields = ['id', 'follower', 'created_at']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id','image']

# class DeviceTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DeviceToken
#         fields = ['token']