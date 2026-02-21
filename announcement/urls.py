from rest_framework.routers import DefaultRouter
from django.urls import path
from .viewsets import *
from .views import *


router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
# router.register(r'sub-category', SubCategoryViewSet, basename='sub-category')
router.register(r'region', RegionViewSet, basename='region')
router.register(r'model',ModelViewSet,basename='model')
router.register(r'image', ImageViewSet, basename='image')
router.register(r"product", ProductViewSet, basename='product')
router.register(r"like", FavoriteViewSet, basename='like')
router.register(r"dislike", DislikeViewSet, basename='dislike')
router.register(r"recently", RecentlyViewSet, basename='recently')
router.register(r"complaint", ComplaintViewSet, basename='complaint')
router.register(r"pricewatch", PriceWatchViewSet, basename='pricewatch')
urlpatterns = [
    path('get-category/', get_category),
    path('get-sub-category/<int:pk>/', get_sub_category),
    path('get-sub-sub-category/<int:pk>/', get_sub_sub_category),
    path('get-region/', get_region),
    path('get-money-type/', get_money_type),
    path('all-statistic/', all_statistic),
    

    # path('get-sold/', get_sold),
    
]

urlpatterns += router.urls