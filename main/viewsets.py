from announcement.serializers import ImageSerializer, ProductSerializer
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import F , Prefetch, Count
from rest_framework.decorators import action
from rest_framework.response import Response
from announcement.decorators import IsStaff
from rest_framework import viewsets
from rest_framework import status
from .serializers import *
from .models import *
import datetime

class Paginator(PageNumberPagination):
    page_size = 25

class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            following_id = request.data.get('following_id')
            follow_, created = UserFollow.objects.get_or_create(
                follower=user,
                following_id=following_id
            )
            if created:
                return Response({'success':True},status=201) 

            follow_.delete()
            return Response({'success':False},status=204)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


    @action(detail=False, methods=['get'])
    def following(self, request): # men obuna boldim 
        user = request.user

        qs = UserFollow.objects.filter(
            follower=user
        ).select_related('following')

        serializer = FollowingSerializer(qs, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def followers(self, request): # meni obunachilarim
        user = request.user

        qs = UserFollow.objects.filter(
            following=user
        ).select_related('follower')

        serializer = FollowerSerializer(qs, many=True)
        return Response(serializer.data)

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']
    # pagination_class = Paginator
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.image:
            obj.image.delete(save=False)  # faylni o‘chiradi

        obj.delete()  # DB recordni o‘chiradi
        return Response({'success': True})
        
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    pagination_class = Paginator
    serializer_class = UserSerializer
    permission_classes = [IsStaff]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filterset_fields = ['is_active', 'is_staff']
    search_fields = ['first_name', 'last_name', 'phone']
    ordering_fields = ['id', 'first_name', 'last_name']
    ordering = ['-id']

class AdminImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    pagination_class = Paginator
    serializer_class = ImageSerializer
    permission_classes = [IsStaff]
    http_method_names = ['get', 'delete']
    filterset_fields = ['user']
    search_fields = ['user__first_name', 'user__last_name',]
    ordering_fields = ['id', 'created_at']
    ordering = ['-id']
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.image.delete(save=False)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = Paginator
    serializer_class = ProductSerializer
    permission_classes = [IsStaff]
    http_method_names = ['get', 'delete']
    filterset_fields = ['is_active', 'category', 'owner','model']
    search_fields = ['title', 'description','category__name', 'model__name']
    ordering_fields = ['id', 'title', 'created_at']
    ordering = ['-id']

    @action(detail=False, methods=['get'])
    def is_active(self, request):
        date = datetime.datetime.now() - datetime.timedelta(days=5)
        product = Product.objects.filter(is_active=False,sold='not_sold', created_at__lte=date)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def is_active_true(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product.is_active = True
        product.save()
        return Response({'success': True},status=200)

    @action(detail=True, methods=['post'])
    def is_active_false(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product.is_active = False
        product.save()
        return Response({'success': True},status=200)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for img in instance.image.all():
            img.image.delete(save=False)
            img.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
class AdminChatRoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaff]
    http_method_names = ['get','delete']
    def get_queryset(self):
        return ChatRoom.objects.all().annotate(
            message_count=Count('messages')
        ).select_related('user_1', 'user_2', 'owner', 'product').order_by('-created_at').prefetch_related(
            Prefetch('messages', queryset=Message.objects.order_by('-created_at'))
        )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(queryset, request)
        serializer = ChatRoomSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ChatRoomSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):    
        instance = self.get_object()
        messages = instance.messages.all()
        if messages.exists():
            messages.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaff]
    def get_queryset(self):
        return Message.objects.all().select_related('chat_room', 'sender').order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = PageNumberPagination()
        paginator.page_size = 50
        page = paginator.paginate_queryset(queryset, request)
        serializer = MessageSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MessageSerializer(instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)