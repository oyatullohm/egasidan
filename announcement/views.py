from ast import Is
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from rest_framework.response import Response
from decimal import InvalidOperation
from .decorators import IsStaff
from .serializers import *
from .models import *
from django.core.cache import cache
from main.models import CustomUser, UserFollow




@api_view(["GET"])
@permission_classes([AllowAny])
def all_statistic(request):
    data = cache.get("all_statistic")

    if not data:
        data = Product.objects.aggregate(
            all_count=Count('id'),
            active_count=Count('id', filter=Q(is_active=True)),
            inactive_count=Count('id', filter=Q(is_active=False)),
        )
        data["user_count"] = CustomUser.objects.count()
        cache.set("all_statistic", data, 60*10)  # 10 minutes

    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny]) 
def get_category(request):
    category = Category.objects.filter(level=1).prefetch_related('models')
    serializer = CategorySerializer(category, many=True )
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny]) 
def get_sub_category(request, pk):
    # category = Category.objects.get(id=pk)
    sub_category = Category.objects.filter(category_id=pk).select_related('category').prefetch_related('models')
    serializer = CategorySerializer(sub_category, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny]) 
def get_sub_sub_category(request, pk):
    sub_category = Category.objects.filter(category_id=pk).select_related('category','category__category').prefetch_related('models')
    serializer = CategorySerializer(sub_category, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_region(request):
    region = Region.objects.all()
    serializer = RegionSerializer(region, many=True )
    return Response(serializer.data)

@api_view(["GET"])
def get_money_type(request):
    return Response([{'name': i[0], 'value': i[1]} for i in Product.MONEY_CHOICES])


