from rest_framework.routers import DefaultRouter
from django.urls import path
from .viewsets import *
from .views import *


router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'sub-category', SubCategoryViewSet, basename='sub-category')
router.register(r'region', RegionViewSet, basename='region')
router.register(r'district', DistrictViewSet, basename='district')
router.register(r'vehicle', VehicleViewSet, basename='vehicle')
router.register(r'image', ImageViewSet, basename='image')
router.register(r'brand', BrandViewSet, basename='carbrand')
router.register(r'model', ModellViewSet, basename='carmodel')
router.register(r"service", ServiceViewSrt, basename='service')
router.register(r"property", PropertyViewSet, basename='property')
router.register(r"electronic", ElectronicsViewSet, basename='electronic')
router.register(r"job", JobViewSet, basename='job')
router.register(r"sport", SportingGoodsViewSet, basename='sport')
router.register(r"hourse", HouseholdItemsViewSet, basename='hourse')
router.register(r"pet", PetViewSet, basename='pet')
router.register(r"like", FavoriteViewSet, basename='like')
router.register(r"dislike", DislikeViewSet, basename='dislike')

urlpatterns = [
    path('get-category/', get_category),
    path('get-sub-category/<int:pk>/', get_sub_category),
    path('get-district/<int:pk>/', get_district),
    path('get-region/', get_region),
    path('get-condition/', get_condition),
    path('get-vehicle-type/', get_vehicle_type),
    path('get-fuel-type/', get_fuel_type),
    path('get-transmission/', get_transmission),
    path('get-property-type/', get_property_type),
    path('get-job-type/', get_job_type),
    path('get-service-type/', get_service_type),
    path('get-hoursehold-type/', get_hoursehold_type),
    path('get-sport-type/', get_sport_type),
    path('get-animal-type/', get_animal_type),
    
    path('get-brand/', get_brand),
    path('get-model/<int:pk>/', get_model),
    path('get-brand-type/', get_brand_type),
    path('is-active-true-false/', is_acttive_true_false),
    # path('get-sold/', get_sold),
    
]

urlpatterns += router.urls