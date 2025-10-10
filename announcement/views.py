
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import  AllowAny, IsAuthenticated
from .decorators import IsStaff
from rest_framework.pagination import PageNumberPagination

@api_view(["GET"])
@permission_classes([IsStaff])
def announcements_all_statistic(request):
    model_list = [
        Vehicle,
        Property,
        Electronics,
        Job,
        Service,
        HouseholdItems,
        SportingGoods,
        Pet]

    all_count = 0
    active_count = 0
    inactive_count = 0
    for model in model_list:
        queryset = model.objects.all().select_related('category')
        all_count += queryset.count()
        active_count += queryset.filter(is_active=True).count()
        inactive_count += queryset.filter(is_active=False).count()
    
    user = User.objects.count()
    complaint = Complaint.objects.count()
    
    return Response({
        "all_count": all_count,
        "active_count": active_count,
        "inactive_count": inactive_count,
        "user_count": user,
        "complaint_count": complaint
        
    })
    
@api_view(["GET"])
def announcements_all(request):
    filters = {"is_active": True}

    # query_params tekshirish
    district = request.query_params.get("district")
    if district:
        filters["district_id"] = district

    region = request.query_params.get("region")
    if region:
        filters["district__region_id"] = region
    
    category = request.query_params.get('category')
    if category:
        filters['category__category'] = category
    
    sub_category = request.query_params.get('sub-category')
    if sub_category:
        filters['category'] = sub_category
    
    price = request.query_params.get('price')
    if price:
        try:
            price = int(price)
            filters['price__gte'] = price - 50000   # masalan 25 mingdan past 20 ming
            filters['price__lte'] = price + 50000  # yuqoriga 30 ming
        except : pass
            

    
    model_serializer_map = [
        (Vehicle, VehiclelistSerializer),
        (Property, PropertylistSerializer),
        (Electronics, ElectronicslistSerializer),
        (Job, JoblistSerializer),
        (Service, ServicelistSerializer),
        (HouseholdItems, HouseholdItemslistSerializer),
        (SportingGoods, SportingGoodslistSerializer),
        (Pet, PetlistSerializer),
    ]

    all_data = []
    for model, serializer in model_serializer_map:
        queryset = model.objects.filter(**filters).select_related('category').order_by("-id")
        serialized = serializer(queryset, many=True).data
        if serialized:
            all_data += serialized

    # Paginatsiya
    paginator = PageNumberPagination()
    paginator.page_size = 5 # har bir sahifada 20 tadan
    result_page = paginator.paginate_queryset(all_data, request)

    return paginator.get_paginated_response(result_page)

@api_view(["GET"])
def announcements_all_false(request):
    filters = {"is_active": False}

    # query_params tekshirish
    district = request.query_params.get("district")
    if district:
        filters["district_id"] = district

    region = request.query_params.get("region")
    if region:
        filters["district__region_id"] = region
    
    category = request.query_params.get('category')
    if category:
        filters['category__category'] = category
    
    sub_category = request.query_params.get('sub-category')
    if sub_category:
        filters['category'] = sub_category
    
    price = request.query_params.get('price')
    if price:
        try:
            price = int(price)
            filters['price__gte'] = price - 50000   # masalan 25 mingdan past 20 ming
            filters['price__lte'] = price + 50000  # yuqoriga 30 ming
        except : pass
            

    
    model_serializer_map = [
        (Vehicle, VehiclelistSerializer),
        (Property, PropertylistSerializer),
        (Electronics, ElectronicslistSerializer),
        (Job, JoblistSerializer),
        (Service, ServicelistSerializer),
        (HouseholdItems, HouseholdItemslistSerializer),
        (SportingGoods, SportingGoodslistSerializer),
        (Pet, PetlistSerializer),
    ]

    all_data = []
    for model, serializer in model_serializer_map:
        queryset = model.objects.filter(**filters).select_related('category').order_by("-id")
        serialized = serializer(queryset, many=True).data
        if serialized:
            all_data += serialized

    # Paginatsiya
    paginator = PageNumberPagination()
    paginator.page_size = 5 # har bir sahifada 20 tadan
    result_page = paginator.paginate_queryset(all_data, request)

    return paginator.get_paginated_response(result_page)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def announcements_user(request):
    vehicel = Vehicle.objects.filter(user=request.user).order_by('-id')
    property = Property.objects.filter(user=request.user).order_by('-id')
    electronic = Electronics.objects.filter(user=request.user).order_by('-id')
    job =  Job.objects.filter(user=request.user).order_by('-id')
    service = Service.objects.filter(user=request.user).order_by('-id')
    hourse = HouseholdItems.objects.filter(user=request.user).order_by('-id')
    sport = SportingGoods.objects.filter(user=request.user).order_by('-id')
    pet = Pet.objects.filter(user=request.user).order_by('-id')
    
    data = []
    if vehicel:
        data +=VehiclelistSerializer(vehicel, many = True).data,
    if property:
        data += PropertylistSerializer(property, many = True).data,
    if electronic:
        data += ElectronicslistSerializer(electronic, many = True).data,
    if job:
        data += JoblistSerializer(job, many = True).data,
    if service:
        data += ServicelistSerializer(service, many = True).data,
    if hourse:
        data += HouseholdItemslistSerializer(hourse, many = True).data,
    if sport:
        data += SportingGoodslistSerializer(sport, many = True).data,
    if pet:
        data += PetlistSerializer(pet, many = True).data,  

           
    return Response(
        {
          'data': data
        }
    ) 


@api_view(["POST"])
@permission_classes([IsStaff])
def is_acttive_true_false(request):
    try:
        obj_id = request.data['id']
        content_type_id = request.data['content_type']
        content_type = ContentType.objects.get(id=content_type_id) 
        model_class = content_type.model_class()
        obj = model_class.objects.get(id=obj_id)
        obj.is_active = not obj.is_active
        obj.save()
        return Response({"success": True
                         ,"is_active": obj.is_active})
    
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=400)



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
    type = request.query_params.get('type')
    if type:
        carbrand = Brand.objects.filter(type=type)
        serializer = BrandSerializer(carbrand, many=True )
        return Response(serializer.data)
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
    return Response([{"name":i[0], 'value':i[1]} for i in SportingGoods.SPORT_TYPE])

@api_view(['GET'])
def get_animal_type(request):
    return Response([{"name":i[0], 'value':i[1]} for i in Pet.ANIMAL_TYPE])