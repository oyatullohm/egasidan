
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import  AllowAny, IsAuthenticated

@api_view(["GET"])
@permission_classes([AllowAny]) 
def get_category(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True )
    return Response(serializer.data)

@api_view(["GET"])
def get_sub_category(request,pk):
    category = SubCategory.objects.filter(category_id=pk).select_related('category')
    serializer = SubCategorySerializer(category, many=True )
    return Response(serializer.data)


@api_view(["GET"])
def get_region(request):
    region = Region.objects.all()
    serializer = RegionSerializer(region, many=True )
    return Response(serializer.data)


@api_view(["GET"])
def get_district(request, pk):
    district = District.objects.filter(region_id=pk).select_related('region')
    serializer = DistrictSerializer(district, many=True )
    return Response(serializer.data)


@api_view(['GET'])
def get_brand(request):
    carbrand = Brand.objects.all()
    serializer = BrandSerializer(carbrand, many=True )
    return Response(serializer.data)


@api_view(['GET'])
def get_model(request, pk):
    carmodel = Modell.objects.filter(brand_id=pk).select_related('brand')
    serializer = ModellSerializer(carmodel, many=True )
    return Response(serializer.data)


@api_view(['GET'])
def get_condition(request):
    return Response([{'name': i[0], 'value': i[1]} for i in BaseProduct.CONDITION_CHOICES])

@api_view(['GET'])
def get_vehicle_type(request):
    return Response([{'name': i[0], 'value': i[1]} for i in Vehicle.VEHICLE_TYPES])

@api_view(['GET'])
def get_brand_type(request):
    return Response([{'name': i[0], 'value': i[1]} for i in Brand.BRAND_TYPE])

@api_view(['GET'])
def get_fuel_type(request):
    return Response([{'name': i[0], 'value': i[1]} for i in Vehicle.FUEL_TYPES])

@api_view(['GET'])
def get_transmission(request):
    return Response([{'name': i[0], 'value': i[1]} for i in Vehicle.TRANSMISSION_TYPES])


@api_view(['GET'])
def get_property_type(request):
    return Response([{'name':i[0], 'value':i[1] } for i in Property.PROPERTY_TYPES])


@api_view(['GET'])
def get_job_type(request):
    return Response([{"name":i[0], 'value':i[1]} for i in Job.JOB_TYPES])

@api_view(['GET'])
def get_service_type(request):
    return Response([{"name":i[0], 'value':i[1]} for i in Service.SERVICE_TYPES])

@api_view(['GET'])
def get_hoursehold_type(request):
    return Response([{"name":i[0], 'value':i[1]} for i in HouseholdItems.HOUSEHOLD_TYPES])

@api_view(['GET'])
def get_sport_type(request):
    return Response([{"name":i[0], 'value':i[1]} for i in SportingGoods.SPORTING_GOODS_TYPES])

@api_view(['GET'])
def get_animal_type(request):
    return Response([{"name":i[0], 'value':i[1]} for i in Pet.ANIMAL_TYPES])