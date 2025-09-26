from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from django.db.models import F
from rest_framework import status
from .serializers import *
from .decorators import *
from .models import *
P_NUM = 20

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    http_method_names = ['post', 'put', 'delete'] 
    permission_classes = [IsStaff]

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        img = data.get('img')
        category = Category.objects.create(name=name,img=img)
        return Response({
             'success': True,
            'data': CategorySerializer(category, many = False).data
        })

    def update(self, request, *args, **kwargs):
        try:
            instance = Category.objects.get(id=kwargs['pk'])
        except Category.DoesNotExist:
            return Response({
                "success": False,
                "error": "Category topilmadi"
            }, status=status.HTTP_404_NOT_FOUND)

        # 🔹 oddiy text maydonlarini update qilish
        name = request.data.get("name")
        if name:
            instance.name = name

        if "img" in request.FILES:
            if instance.img and instance.img.name:
                instance.img.delete(save=False)  # eski rasmni o‘chirib tashlaymiz
            instance.img = request.FILES["img"]

        instance.save()

        return Response({
            "success": True,
            "data": {
                "id": instance.id,
                "name": instance.name,
                "img": instance.img.url if instance.img else None
            }
        }, status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            category = Category.objects.get(id=id)
            if category.img:
                try:
                    category.img.delete(save=False)
                except: pass
                    
            category.delete()

            return Response({
                "success": True,
                
            })
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    http_method_names = ['post', 'put', 'delete'] 
    permission_classes = [IsStaff]

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        category_id = data.get('category_id')
        category = SubCategory.objects.create(name=name,category_id=category_id)
        return Response({
             'success': True,
            'data': SubCategorySerializer(category, many = False).data
        })

    def update(self, request, *args, **kwargs):
        data = request.data 
        id = kwargs['pk']
        name = data.get('name')
        
        try:
            category = SubCategory.objects.get(id=id)
            category.name = name
            category.save()
    
            return Response({
                "success": True,
                'data': SubCategorySerializer(category, many = False).data
            })
        except:
            return Response({
                "success": False
            })
    def destroy(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            category = SubCategory.objects.get(id=id)
            category.delete()
            
            return Response({
                "success": True,
                
            })
        except:
            return Response({
                "success": False
            })


class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = RegionSerializer
    http_method_names = ['post', 'put', 'delete'] 
    permission_classes = [IsStaff]

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
       
        region = Region.objects.create(name=name)
        return Response({
             'success': True,
            'data': RegionSerializer(region, many = False).data
        })

    def update(self, request, *args, **kwargs):
        data = request.data 
        id = kwargs['pk']
        name = data.get('name')
     
        try:
            region = Region.objects.get(id=id)
            region.name = name

            region.save()
    
            return Response({
                "success": True,
                'data': RegionSerializer(region, many = False).data
            })
        except:
            return Response({
                "success": False
            })
    def destroy(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            region = Region.objects.get(id=id)
            region.delete()
            
            return Response({
                "success": True,
                
            })
        except:
            return Response({
                "success": False
            })


class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    http_method_names = ['post', 'put', 'delete'] 
    permission_classes = [IsStaff]

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        region_id = data.get('region_id')
        
        district = District.objects.create(name=name,region_id=region_id)
        return Response({
             'success': True,
            'data': DistrictSerializer(district, many = False).data
        })

    def update(self, request, *args, **kwargs):
        data = request.data 
        id = kwargs['pk']
        name = data.get('name')
        try:
            district = District.objects.get(id=id)
            district.name = name
            district.save()
    
            return Response({
                "success": True,
                'data': DistrictSerializer(district, many = False).data
            })
        except:
            return Response({
                "success": False
            })
    def destroy(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            district = District.objects.get(id=id)
            district.delete()
            
            return Response({
                "success": True,
                
            })
        except:
            return Response({
                "success": False
            })


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    http_method_names = ['post', 'put', 'delete'] 
    permission_classes = [IsStaff]

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        type = data.get('type')
       
        brand = Brand.objects.create(name=name,type=type)
        return Response({
             'success': True,
            'data': BrandSerializer(brand, many = False).data
        })

    def update(self, request, *args, **kwargs):
        data = request.data 
        id = kwargs['pk']
        name = data.get('name')
     
        try:
            brand = Brand.objects.get(id=id)
            brand.name = name

            brand.save()
    
            return Response({
                "success": True,
                'data': BrandSerializer(brand, many = False).data
            })
        except:
            return Response({
                "success": False
            })
    def destroy(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            brand = Brand.objects.get(id=id)
            brand.delete()
            
            return Response({
                "success": True,
                
            })
        except:
            return Response({
                "success": False
            })
    

class ModellViewSet(viewsets.ModelViewSet):
    serializer_class = ModellSerializer
    http_method_names = ['post', 'put', 'delete'] 
    permission_classes = [IsStaff]

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        brand_id = data.get('brand_id')
        
        model = Modell.objects.create(name=name,brand_id=brand_id)
        return Response({
             'success': True,
            'data': ModellSerializer(model, many = False).data
        })

    def update(self, request, *args, **kwargs):
        data = request.data 
        id = kwargs['pk']
        name = data.get('name')
        try:
            model = Modell.objects.get(id=id)
            model.name = name
            model.save()
    
            return Response({
                "success": True,
                'data':ModellSerializer(model, many = False).data
            })
        except:
            return Response({
                "success": False
            })
    def destroy(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            model = Modell.objects.get(id=id)
            model.delete()
            
            return Response({
                "success": True,
                
            })
        except:
            return Response({
                "success": False
            })


class ImageViewSet(viewsets.ModelViewSet):
    http_method_names = ['delete']
    def destroy(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            image =  Image.objects.get(id=id)
            if image.user != request.user:
                return Response ({
                    "success":False
                })
            image.image.delete()
            image.delete()
            return Response ({
                "success":True
            })
        except:
            return Response ({
                "success":False
            })


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.filter(is_active=True).order_by('-id')
    
    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = P_NUM
        result_page = paginator.paginate_queryset(self.queryset, request)

        serializer = VehiclelistSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })
        
        
    @action(methods=['get'], detail=False)
    def get(self,request):
        return Response({
            # "name":"str max 55 ",
            "description":"str  max 500  null  ",
            "price":"int",
            "old_price":"int  null",
            "condition":"str  name  url: /api/product/get-condition/    ",
            # "sold":"str  name  url: /api/product/get-sold/    ",
            "category":"int  sub-category id  url /api/product/sub-category/1/  1 bu category id url :/api/product/get-category/ ",
            "district":"int  district id url : /api/product/get-district/1/  1 bu region id url : /api/product/get-region/",
            "image":"file  jpg  png " ,
            "address":"str  max 500  null " ,
            "produced": "2025-09-01  null  ",
            "phone_number": "+998900601044",
            "vehicle_type": "str  url :/api/product/get-vehicle-type/",
            "brand": "str  url :/api/product/get-brand/",
            "model": "int  url :/api/product/get-model/1/",
            "mileage": "int  250000  kl ",
            "engine_size": "str  2.5 dvigatel_hajmi ",
            "fuel_type": "str  url :/api/product/get-fuel-type/",
            "transmission": "str  url :/api/product/get-transmission/",
            "color": "str  max 40 ",
        })


    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        vehicle = self.get_object()
         
        if request.user.id != vehicle.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        count =  vehicle.image.all().count()
        if count >= 5:
          return Response({
                'success':False,
                'limit':'5 ta rasmgacha yuklash mumkin',
                'count':count
            }) 
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user) 
            vehicle.image.add(img)
            return Response({
                'success': True,
                'data': VehicleSerializer(vehicle, many = False).data
            })
        return Response({
            'success': False,
            'error': 'Image not provided'
        })
    
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        vehicle = self.get_object()
        if request.user.id != vehicle.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        vehicle.sold = 'sold'
        vehicle.is_active = False
        vehicle.save()
        return Response({
            'success': True,
            'data': VehicleSerializer(vehicle, many = False).data
        })
        
        
    def retrieve(self, request, *args, **kwargs):
        try:
            vehicle = Vehicle.objects.get(id=kwargs['pk'])
        except Vehicle.DoesNotExist:
            return Response({"detail": "Vehicle not found."}, status=404)

        # Atomik inkrement (race condition bo‘lmasligi uchun)
        Vehicle.objects.filter(id=vehicle.id).update(views_count=F('views_count') + 1)
        vehicle.refresh_from_db()

        serializer = VehicleSerializer(vehicle, context={'request': request})
        return Response(serializer.data)


    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            permission_classes = [AllowAny]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


    def create(self, request, *args, **kwargs):
        
        data = request.data
        description = data.get('description')
        price = data.get('price')
        condition =data.get('condition')
        category =data.get('category')
        district =data.get('district')
        image = request.FILES.get('image')
        address =data.get('address')
        produced =data.get('produced')
        phone_number =data.get('phone_number')
        vehicle_type =data.get('vehicle_type')
        brand =data.get('brand')
        model =data.get('model')
        # year =data.get('year')
        mileage =data.get('mileage')
        engine_size =data.get('engine_size')
        fuel_type =data.get('fuel_type')
        transmission =data.get('transmission')
        color =data.get('color')
        
        vehicle = Vehicle.objects.create(
            user = request.user,
            description = description,
            price = price,
            condition = condition,
            category_id = category,
            district_id = district, 
            address = address,
            produced = produced,
            phone_number = phone_number,
            vehicle_type = vehicle_type,
            brand = brand,
            model_id = model,
            # year = year,
            mileage = mileage,
            engine_size = engine_size,
            fuel_type = fuel_type,
            transmission = transmission,
            color = color)
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user)  # `Image` modelida `file = models.ImageField(...)` bo‘lishi kerak
            vehicle.image.add(img)
        return Response({
                'success': True,
                'data': VehicleSerializer(vehicle, many = False).data
            })

    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.id != instance.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            serializer = self.get_serializer(instance, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "data": serializer.data
                })
            return Response({
                "success": False,
                "errors": serializer.errors
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    
    def destroy(self, request, *args, **kwargs):
        try:
            vehicle = self.get_object()  
            if request.user.id != vehicle.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            images = list(vehicle.image.all()) 
            vehicle.delete()
            for img in images:
                if not img.vehicle_set.exists():
                    img.delete()

            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.filter(is_active=True).order_by('-id')
    
    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = P_NUM
        result_page = paginator.paginate_queryset(self.queryset, request)

        serializer = PropertylistSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })
    
    @action(methods=['get'], detail=False)
    def get(self,request):
        return Response({
            # "name":"str max 55 ",
            "description":"str  max 500  null  ",
            "price":"int",
            "old_price":"int  null",
            "condition":"str  name  url: /api/product/get-condition/    ",
            # "sold":"str  name  url: /api/product/get-sold/    ",
            "category":"int  sub-category id  url /api/product/sub-category/1/  1 bu category id url :/api/product/get-category/ ",
            "district":"int  district id url : /api/product/get-district/1/  1 bu region id url : /api/product/get-region/",
            "image":"file  jpg  png " ,
            "address":"str  max 500  null " ,
            "produced": "2025-09-01  null  ",
            "phone_number": "+998900601044",
            "property_type": "str  url :/api/product/get-property-type/",
            "rooms": "int 3",
            "area": "int 250   m2",
        })
    
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        property = self.get_object()
        if request.user.id != property.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        count =  property.image.all().count()
        if count >= 5:
          return Response({
                'success':False,
                'limit':'5 ta rasmgacha yuklash mumkin',
                'count':count
            }) 
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user) 
            property.image.add(img)
            return Response({
                'success': True,
                'data': PropertySerializer(property, many = False).data
            })
        return Response({
            'success': False,
            'error': 'Image not provided'
        })
    
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        property = self.get_object()
        if request.user.id != property.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        property.sold = 'sold'
        property.is_active = False
        property.save()
        return Response({
            'success': True,
            'data': PropertySerializer(property, many = False).data
        })
    
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            permission_classes = [AllowAny]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
           
    def retrieve(self, request, *args, **kwargs):
        try:
            property= Property.objects.get(id=kwargs['pk'])
        except Property.DoesNotExist:
            return Response({"detail": "property not found."}, status=404)

        # Atomik inkrement (race condition bo‘lmasligi uchun)
        Property.objects.filter(id=property.id).update(views_count=F('views_count') + 1)
        property.refresh_from_db()

        serializer = PropertySerializer(property, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        description = data.get('description')
        price = data.get('price')
        old_price = data.get('old_price')
        condition =data.get('condition')
        category =data.get('category')
        district =data.get('district')
        image =data.get('image')
        address =data.get('address')
        produced =data.get('produced')
        phone_number =data.get('phone_number')
        property_type =data.get('property_type')
        rooms =data.get('rooms')
        area =data.get('area')   
        property = Property.objects.create(
            user = request.user,
            description = description,
            price = price,
            old_price = old_price,
            condition = condition,
            category_id = category,
            district_id = district, 
            address = address,  
            produced = produced,
            phone_number = phone_number,
            property_type = property_type,
            rooms = rooms,
            area = area
            )
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user)  # `Image` modelida `file = models.ImageField(...)` bo‘lishi kerak
            property.image.add(img)
        return Response({
                'success': True,
                'data': PropertySerializer(property, many = False).data
            })  
     
        
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.id != instance.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            serializer = self.get_serializer(instance, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "data": serializer.data
                })
            return Response({
                "success": False,
                "errors": serializer.errors
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    
    def destroy(self, request, *args, **kwargs):
        try:
            property = self.get_object()  
            if request.user.id != property.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            images = list(property.image.all()) 
            property.delete()
            for img in images:
                if not img.property_set.exists():
                    img.delete()

            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })


class ElectronicsViewSet(viewsets.ModelViewSet):
    serializer_class = ElectronicsSerializer
    queryset = Electronics.objects.filter(is_active=True).order_by('-id')
    
    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = P_NUM
        result_page = paginator.paginate_queryset(self.queryset, request)

        serializer = ElectronicslistSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })
    
    
    def create(self, request, *args, **kwargs):
        data = request.data
        description = data.get('description')
        price = data.get('price')
        old_price = data.get('old_price')
        condition =data.get('condition')
        category =data.get('category')
        district =data.get('district')
        image =request.FILES.get('image') 
        address =data.get('address')
        produced =data.get('produced')
        phone_number =data.get('phone_number')
        electronic_type = data.get('electronic_type')
        brand = data.get('brand')
        model = data.get('model')
        warranty = data.get('warranty')
        warranty_months = data.get('warranty_months')
        
        electronics = Electronics.objects.create(
            user = request.user,
            description = description,
            price = price,
            old_price = old_price,
            condition = condition,
            category_id = category,
            district_id = district,
            address = address,
            produced = produced,
            phone_number = phone_number,
            electronic_type = electronic_type,
            brand = brand,
            model = model,
            warranty = warranty,
            warranty_months = warranty_months
            
            )
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user)  # `Image` modelida `file = models.ImageField(...)` bo‘lishi kerak
            electronics.image.add(img)
        return Response({
                'success': True,
                'data': ElectronicsSerializer(electronics, many = False).data
            })
    
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.id != instance.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            serializer = self.get_serializer(instance, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "data": serializer.data
                })
            return Response({
                "success": False,
                "errors": serializer.errors
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    
    def destroy(self, request, *args, **kwargs):
        try:
            electronics = self.get_object()  
            if request.user.id != electronics.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            images = list(electronics.image.all()) 
            electronics.delete()
            for img in images:
                if not img.electronics_set.exists():
                    img.delete()

            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    @action(methods=['get'], detail=False)
    def get(self,request):
        return Response({
            # "name":"str max 55 ",
            "description":"str  max 500  null  ",
            "price":"int",
            "old_price":"int  null",
            "condition":"str  name  url: /api/product/get-condition/    ",
            # "sold":"str  name  url: /api/product/get-sold/    ",
            "category":"int  sub-category id  url /api/product/sub-category/1/  1 bu category id url :/api/product/get-category/ ",
            "district":"int  district id url : /api/product/get-district/1/  1 bu region id url : /api/product/get-region/",
            "image":"file  jpg  png " ,
            "address":"str  max 500  null " ,
            "produced": "2025-09-01  null  ",
            "phone_number": "+998900601044",
            "electronic_type": "str  url :/api/product/get-electronic-type/",
            "brand": "str max 100 ",
            "model": "str max 100 ",
            "warranty": "bool True False ",
            "warranty_months": "int   null "
        })
    
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            permission_classes = [AllowAny]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    
            
    def retrieve(self, request, *args, **kwargs):
        try:
            electronic = Electronics.objects.get(id=kwargs['pk'])
        except Electronics.DoesNotExist:
            return Response({"detail": "electronic not found."}, status=404)

        # Atomik inkrement (race condition bo‘lmasligi uchun)
        Electronics.objects.filter(id=electronic.id).update(views_count=F('views_count') + 1)
        electronic.refresh_from_db()

        serializer = ElectronicsSerializer(electronic, context={'request': request})
        return Response(serializer.data)
   
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        electronics = self.get_object()
        if request.user.id != electronics.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        count =  electronics.image.all().count()
        if count >= 5:
          return Response({
                'success':False,
                'limit':'5 ta rasmgacha yuklash mumkin',
                'count':count
            }) 
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user) 
            electronics.image.add(img)
            return Response({
                'success': True,
                'data': ElectronicsSerializer(electronics, many = False).data
            })
        return Response({
            'success': False,
            'error': 'Image not provided'
        })
    
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        electronics = self.get_object()
        if request.user.id != electronics.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        electronics.sold = 'sold'
        electronics.is_active = False
        electronics.save()
        return Response({
            'success': True,
            'data': ElectronicsSerializer(electronics, many = False).data
        })  


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.filter(is_active=True).order_by('-id')
    
    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = P_NUM
        result_page = paginator.paginate_queryset(self.queryset, request)

        serializer = JoblistSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        data = request.data
        description = data.get('description')
        price = data.get('price')
        old_price = data.get('old_price')
        # condition =data.get('condition')
        category =data.get('category')
        district =data.get('district')
        image =request.FILES.get('image') 
        address =data.get('address')
        telegram =data.get('telegram')
        phone_number =data.get('phone_number')
        job_type = data.get('job_type')
        company = data.get('company')
        application_deadline = data.get('application_deadline')
        remote_work = data.get('remote_work')
        job = Job.objects.create(
            user = request.user,
            description = description,
            price = price,
            old_price = old_price,
            # condition = condition,
            category_id = category,
            district_id = district,
            address = address,
            phone_number = phone_number,
            telegram = telegram,
            job_type = job_type,
            company = company,
            application_deadline = application_deadline,
            remote_work = remote_work
            )
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user)  # `Image` modelida `file = models.ImageField(...)` bo‘lishi kerak
            job.image.add(img)
        return Response({
                'success': True,
                'data': JobSerializer(job, many = False).data
            })
    
            
    def retrieve(self, request, *args, **kwargs):
        try:
            job = Job.objects.get(id=kwargs['pk'])
        except Job.DoesNotExist:
            return Response({"detail": "job not found."}, status=404)

        # Atomik inkrement (race condition bo‘lmasligi uchun)
        Job.objects.filter(id=job.id).update(views_count=F('views_count') + 1)
        job.refresh_from_db()

        serializer = JobSerializer(job, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.id != instance.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            serializer = self.get_serializer(instance, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "data": serializer.data
                })
            return Response({
                "success": False,
                "errors": serializer.errors
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    def destroy(self, request, *args, **kwargs):
        try:
            job = self.get_object()  
            if request.user.id != job.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            images = list(job.image.all()) 
            job.delete()
            for img in images:
                if not img.job_set.exists():
                    img.delete()

            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    @action(methods=['get'], detail=False)
    def get(self,request):
        return Response({
            # "name":"str max 55 ",
            "description":"str  max 500  null  ",
            "price":"int",
            "old_price":"int  null",
            "condition":"str  name  url: /api/product/get-condition/    ",
            # "sold":"str  name  url: /api/product/get-sold/    ",
            "category":"int  sub-category id  url /api/product/sub-category/1/  1 bu category id url :/api/product/get-category/ ",
            "district":"int  district id url : /api/product/get-district/1/  1 bu region id url : /api/product/get-region/",
            "image":"file  jpg  png " ,
            "address":"str  max 500  null " ,
            "telegram": "str  max 100  null  telegram username @username  ",
            "phone_number": "+998900601044",
            "job_type": "str  url :/api/product/get-job-type/",
            "company": "str max 100 ",
            "application_deadline": "2025-09-01   null ",
            "remote_work": "bool True False "
        })
   
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        job = self.get_object()
        if request.user.id != job.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        count =  job.image.all().count()
        if count >= 5:
          return Response({
                'success':False,
                'limit':'5 ta rasmgacha yuklash mumkin',
                'count':count
            }) 
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user) 
            job.image.add(img)
            return Response({
                'success': True,
                'data': JobSerializer(job, many = False).data
            })
        return Response({
            'success': False,
            'error': 'Image not provided'
        }) 
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        job = self.get_object()
        if request.user.id != job.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        job.sold = 'sold'
        job.is_active = False
        job.save()
        return Response({
            'success': True,
            'data': JobSerializer(job, many = False).data
        })
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            permission_classes = [AllowAny]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    

class ServiceViewSrt(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.filter(is_active=True).order_by('-id')
    
    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = P_NUM
        result_page = paginator.paginate_queryset(self.queryset, request)

        serializer = ServicelistSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        data = request.data
        description = data.get('description')
        price = data.get('price')
        old_price = data.get('old_price')
        # condition =data.get('condition')
        category =data.get('category')
        district =data.get('district')
        image =request.FILES.get('image') 
        address =data.get('address')
        phone_number =data.get('phone_number')
        service_type= data.get('service_type')
        experience_years = data.get('experience_years')
        availability = data.get('availability')
        
        service = Service.objects.create(
            user=request.user,
            description=description,
            price=price,
            old_price=old_price,
            # condition = condition,
            category_id=category,
            district_id=district,
            address=address,
            phone_number=phone_number,
            service_type=service_type,
            experience_years=experience_years,
            availability=availability  
        )
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user)  # `Image` modelida `file = models.ImageField(...)` bo‘lishi kerak
            service.image.add(img)
        return Response({
                'success': True,
                'data': ServiceSerializer(service, many = False).data
            })
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        service = self.get_object()
        if request.user.id != job.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        count =  service.image.all().count()
        if count >= 5:
          return Response({
                'success':False,
                'limit':'5 ta rasmgacha yuklash mumkin',
                'count':count
            }) 
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user) 
            service.image.add(img)
            return Response({
                'success': True,
                'data': JobSerializer(service, many = False).data
            })
        return Response({
            'success': False,
            'error': 'Image not provided'
        }) 
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        service = self.get_object()
        if request.user.id != job.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        service.sold = 'sold'
        service.is_active = False
        service.save()
        return Response({
            'success': True,
            'data': ServiceSerializer(service, many = False).data
        })
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            permission_classes = [AllowAny]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

            
    def retrieve(self, request, *args, **kwargs):
        try:
            service = Service.objects.get(id=kwargs['pk'])
        except Service.DoesNotExist:
            return Response({"detail": "service not found."}, status=404)

        # Atomik inkrement (race condition bo‘lmasligi uchun)
        Service.objects.filter(id=service.id).update(views_count=F('views_count') + 1)
        service.refresh_from_db()

        serializer = ServiceSerializer(service, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.id != instance.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            serializer = self.get_serializer(instance, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "data": serializer.data
                })
            return Response({
                "success": False,
                "errors": serializer.errors
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    def destroy(self, request, *args, **kwargs):
        try:
            service = self.get_object()  
            if request.user.id != job.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            images = list(job.image.all()) 
            service.delete()
            for img in images:
                if not img.service.exists():
                    img.delete()

            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
            
    @action(methods=['get'], detail=False)
    def get(self,request):
        return Response({
            # "name":"str max 55 ",
            "description":"str  max 500  null  ",
            "price":"int",
            "old_price":"int  null",
            "condition":"str  name  url: /api/product/get-condition/    ",
            # "sold":"str  name  url: /api/product/get-sold/    ",
            "category":"int  sub-category id  url /api/product/sub-category/1/  1 bu category id url :/api/product/get-category/ ",
            "district":"int  district id url : /api/product/get-district/1/  1 bu region id url : /api/product/get-region/",
            "image":"file  jpg  png " ,
            "address":"str  max 500  null " ,
            "phone_number": "+998900601044",
            "service_type": "str url :/api/product/get-service-type/",
            "experience_years":"int",
            "availability":"boll" 
            
        })
        

class HouseholdItemsViewSet(viewsets.ModelViewSet):
    serializer_class = HouseholdItemsSerializer
    queryset = HouseholdItems.objects.filter(is_active=True).order_by('-id')
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = P_NUM
        result_page = paginator.paginate_queryset(self.queryset, request)

        serializer = HouseholdItemslistSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        data = request.data
        description = data.get('description')
        price = data.get('price')
        old_price = data.get('old_price')
        condition =data.get('condition')
        category =data.get('category')
        district =data.get('district')
        image =request.FILES.get('image') 
        address =data.get('address')
        produced =data.get('produced')
        phone_number =data.get('phone_number')
        hourse_type = data.get('hourse_type')
        model = data.get('model')
        experience_years = data.get('experience_years')
        
        household_item = HouseholdItems.objects.create(
            user = request.user,
            description = description,
            price = price,
            old_price = old_price,
            condition = condition,
            category_id = category,
            district_id = district,
            address = address,
            produced = produced,
            phone_number = phone_number,
            hourse_type = hourse_type,
            model = model,
            experience_years = experience_years
            )
        image = request.FILES.get('image')
        if image:   
            img = Image.objects.create(image=image, user=request.user)  # `Image` modelida `file = models.ImageField(...)` bo‘lishi kerak
            household_item.image.add(img)
        return Response({
                'success': True,
                'data': HouseholdItemsSerializer(household_item, many = False).data
            })

            
    def retrieve(self, request, *args, **kwargs):
        try:
            hourse = HouseholdItems.objects.get(id=kwargs['pk'])
        except HouseholdItems.DoesNotExist:
            return Response({"detail": "hourse not found."}, status=404)

        # Atomik inkrement (race condition bo‘lmasligi uchun)
        HouseholdItems.objects.filter(id=hourse.id).update(views_count=F('views_count') + 1)
        hourse.refresh_from_db()

        serializer = HouseholdItemsSerializer(hourse, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.id != instance.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            serializer = self.get_serializer(instance, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "data": serializer.data
                })
            return Response({
                "success": False,
                "errors": serializer.errors
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })

    def destroy(self, request, *args, **kwargs):
        try:
            household_item = self.get_object()  
            if request.user.id != household_item.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            images = list(household_item.image.all()) 
            household_item.delete()
            for img in images:
                if not img.householditems_set.exists():
                    img.delete()

            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    @action(methods=['get'], detail=False)
    def get(self,request):
        return Response({
            # "name":"str max 55 ",
            "description":"str  max 500  null  ",
            "price":"int",
            "old_price":"int  null",
            "condition":"str  name  url: /api/product/get-condition/    ",
            # "sold":"str  name  url: /api/product/get-sold/    ",
            "category":"int  sub-category id  url /api/product/sub-category/1/  1 bu category id url :/api/product/get-category/ ",
            "district":"int  district id url : /api/product/get-district/1/  1 bu region id url : /api/product/get-region/",
            "image":"file  jpg  png " ,
            "address":"str  max 500  null " ,
            "produced": "2025-09-01  null  ",
            "phone_number": "+998900601044",
            "hourse_type": "str  url :/api/product/get-hoursehold-type/",
            "model": "str max 100 ",
            "experience_years": "int   null "
        })
        
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        household_item = self.get_object()
        if request.user.id != household_item.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        count =  household_item.image.all().count()
        if count >= 5:
          return Response({
                'success':False,
                'limit':'5 ta rasmgacha yuklash mumkin',
                'count':count
            }) 
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user) 
            household_item.image.add(img)
            return Response({
                'success': True,
                'data': HouseholdItemsSerializer(household_item, many = False).data
            })
        return Response({
            'success': False,
            'error': 'Image not provided'
        })
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        household_item = self.get_object()
        if request.user.id != household_item.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        household_item.sold = 'sold'
        household_item.is_active = False
        household_item.save()
        return Response({
            'success': True,
            'data': HouseholdItemsSerializer(household_item, many = False).data
        })
    
    
class SportingGoodsViewSet(viewsets.ModelViewSet):
    serializer_class = SportingGoodsSerializer
    queryset = SportingGoods.objects.filter(is_active=True).order_by('-id')
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = P_NUM
        result_page = paginator.paginate_queryset(self.queryset, request)

        serializer = SportingGoodslistSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        data = request.data
        description = data.get('description')
        price = data.get('price')
        old_price = data.get('old_price')
        condition =data.get('condition')
        category =data.get('category')
        district =data.get('district')
        image =request.FILES.get('image') 
        address =data.get('address')
        produced =data.get('produced')
        phone_number =data.get('phone_number')
        sport_type = data.get('sport_type')
        brand = data.get('brand')
        model = data.get('model')
        
        sporting_goods = SportingGoods.objects.create(
            user = request.user,
            description = description,
            price = price,
            old_price = old_price,
            condition = condition,
            category_id = category,
            district_id = district,
            address = address,
            produced = produced,
            phone_number = phone_number,
            sport_type = sport_type,
            brand = brand,
            model = model
            )
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user)  # `Image` modelida `file = models.ImageField(...)` bo‘lishi kerak
            sporting_goods.image.add(img)
        return Response({
                'success': True,
                'data': SportingGoodsSerializer(sporting_goods, many = False).data
            })
    
            
    def retrieve(self, request, *args, **kwargs):
        try:
            sport = SportingGoods.objects.get(id=kwargs['pk'])
        except SportingGoods.DoesNotExist:
            return Response({"detail": "Vehicle not found."}, status=404)

        # Atomik inkrement (race condition bo‘lmasligi uchun)
        SportingGoods.objects.filter(id=sport.id).update(views_count=F('views_count') + 1)
        sport.refresh_from_db()

        serializer = SportingGoodsSerializer(sport, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.id != instance.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            serializer = self.get_serializer(instance, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "data": serializer.data
                })
            return Response({
                "success": False,
                "errors": serializer.errors
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
   
    def destroy(self, request, *args, **kwargs):
        try:
            sporting_goods = self.get_object()  
            if request.user.id != sporting_goods.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            images = list(sporting_goods.image.all()) 
            sporting_goods.delete()
            for img in images:
                if not img.sportinggoods_set.exists():
                    img.delete()

            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    @action(methods=['get'], detail=False)
    def get(self,request):
        return Response({
            # "name":"str max 55 ",
            "description":"str  max 500  null  ",
            "price":"int",
            "old_price":"int  null",
            "condition":"str  name  url: /api/product/get-condition/    ",
            # "sold":"str  name  url: /api/product/get-sold/    ",
            "category":"int  sub-category id  url /api/product/sub-category/1/  1 bu category id url :/api/product/get-category/ ",
            "district":"int  district id url : /api/product/get-district/1/  1 bu region id url : /api/product/get-region/",
            "image":"file  jpg  png " ,
            "address":"str  max 500  null " ,
            "produced": "2025-09-01  null  ",
            "phone_number": "+998900601044",
            "electronic_type": "str  url :/api/product/get-sport-type/",
            "brand": "str max 100 ",
            "model": "str max 100 "
        })
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        sporting_goods = self.get_object()
        if request.user.id != sporting_goods.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        count =  sporting_goods.image.all().count()
        if count >= 5:
          return Response({
                'success':False,
                'limit':'5 ta rasmgacha yuklash mumkin',
                'count':count
            }) 
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user) 
            sporting_goods.image.add(img)
            return Response({
                'success': True,
                'data': SportingGoodsSerializer(sporting_goods, many = False).data
            })
        return Response({
            'success': False,
            'error': 'Image not provided'
        })
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        sporting_goods = self.get_object()
        if request.user.id != sporting_goods.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        sporting_goods.sold = 'sold'
        sporting_goods.is_active = False
        sporting_goods.save()
        return Response({
            'success': True,
            'data': SportingGoodsSerializer(sporting_goods, many = False).data
        })

    
class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    queryset = Pet.objects.filter(is_active=True).order_by('-id')
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = P_NUM
        result_page = paginator.paginate_queryset(self.queryset, request)

        serializer = PetlistSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        data = request.data
        description = data.get('description')
        price = data.get('price')
        old_price = data.get('old_price')
        condition =data.get('condition')
        category =data.get('category')
        district =data.get('district')
        image =request.FILES.get('image') 
        address =data.get('address')
        phone_number =data.get('phone_number')
        animal_type = data.get('animal_type')
        breed = data.get('breed')
        age = data.get('age')
        
        pet = Pet.objects.create(
            user = request.user,
            description = description,
            price = price,
            old_price = old_price,
            condition = condition,
            category_id = category,
            district_id = district,
            address = address,
            phone_number = phone_number,
            animal_type = animal_type,
            breed = breed,
            age = age
            )
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user)
            pet.image.add(img)  # `Image` modelida `file = models.ImageField(...)` bo‘lishi kerak
        return Response({   
                'success': True,
                'data': PetSerializer(pet, many = False).data
            })
    
            
    def retrieve(self, request, *args, **kwargs):
        try:
            pet = Pet.objects.get(id=kwargs['pk'])
        except Pet.DoesNotExist:
            return Response({"detail": "Vehicle not found."}, status=404)

        # Atomik inkrement (race condition bo‘lmasligi uchun)
        Pet.objects.filter(id=pet.id).update(views_count=F('views_count') + 1)
        pet.refresh_from_db()

        serializer = PetSerializer(pet, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.id != instance.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            serializer = self.get_serializer(instance, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "data": serializer.data
                })
            return Response({
                "success": False,
                "errors": serializer.errors
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
    
    def destroy(self, request, *args, **kwargs):
        try:
            pet = self.get_object()  
            if request.user.id != pet.user.id:
                return Response({
                    'success':False,
                    'permissions':False
                })
            images = list(pet.image.all()) 
            pet.delete()
            for img in images:
                if not img.pet_set.exists():
                    img.delete()

            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })
   
    @action(methods=['get'], detail=False)
    def get(self,request):
        return Response({
            # "name":"str max 55 ",
            "description":"str  max 500  null  ",
            "price":"int",
            "old_price":"int  null",
            "condition":"str  name  url: /api/product/get-condition/    ",
            # "sold":"str  name  url: /api/product/get-sold/    ",
            "category":"int  sub-category id  url /api/product/sub-category/1/  1 bu category id url :/api/product/get-category/ ",
            "district":"int  district id url : /api/product/get-district/1/  1 bu region id url : /api/product/get-region/",
            "image":"file  jpg  png " ,
            "address":"str  max 500  null " ,
            "phone_number": "+998900601044",
            "animal_type": "str  url :/api/product/get-animal-type/",
            "breed": "str max 100 ",
            "age": "int   null "
        })
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        pet = self.get_object()
        if request.user.id != pet.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        count =  pet.image.all().count()
        if count >= 5:
          return Response({
                'success':False,
                'limit':'5 ta rasmgacha yuklash mumkin',
                'count':count
            }) 
        image = request.FILES.get('image')
        if image:
            img = Image.objects.create(image=image, user=request.user) 
            pet.image.add(img)
            return Response({
                'success': True,
                'data': PetSerializer(pet, many = False).data
            })
        return Response({
            'success': False,
            'error': 'Image not provided'
        })
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        pet = self.get_object()
        if request.user.id != pet.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        pet.sold = 'sold'
        pet.is_active = False
        pet.save()
        return Response({
            'success': True,
            'data': PetSerializer(pet, many = False).data
        })
    

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer 
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        
        return Response({
            "success": True,
            "data": FavoriteSerializer(self.get_queryset(), many=True).data
        })

    @action(methods=['get'], detail=False)
    def count(self, request):
        user = request.user
        favorite_count = Favorite.objects.filter(user=user).count()
        return Response({
            'success': True,
            'favorite_count': favorite_count
        })
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("user").order_by('-id')

    def create(self, request, *args, **kwargs):
        data = request.data
        content_type = data.get('content_type')  # masalan: "job"
        object_id = data.get('object_id')

        try:
            content_type = ContentType.objects.get(id=content_type)
           
        except ContentType.DoesNotExist:
            return Response({'success': False, 'message': 'Noto‘g‘ri content_type'}, status=400)

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id
        )

        if not created:
            return Response({
                'success': False,
                'message': "hatolik: Bu mahsulot allaqachon sevimlilarga qo'shilgan."
            })

        return Response({'success': True, 'message': 'Sevimlilarga qo‘shildi'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Favorite item removed successfully.'
        })


class DislikeViewSet(viewsets.ModelViewSet):
    serializer_class = DislikeSerializer 
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        
        return Response({
            "success": True,
            "data": DislikeSerializer(self.get_queryset(), many=True).data
        })

    @action(methods=['get'], detail=False)
    def count(self, request):
        user = request.user
        favorite_count = Dislike.objects.filter(user=user).count()
        return Response({
            'success': True,
            'dislike_count': favorite_count
        })
    
    def get_queryset(self):
        return Dislike.objects.filter(user=self.request.user).select_related("user").order_by('-id')

    def create(self, request, *args, **kwargs):
        data = request.data
        content_type = data.get('content_type')  # masalan: "job"
        object_id = data.get('object_id')

        try:
            content_type = ContentType.objects.get(id=content_type)
           
        except ContentType.DoesNotExist:
            return Response({'success': False, 'message': 'Noto‘g‘ri content_type'}, status=400)

        favorite, created = Dislike.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id
        )

        if not created:
            return Response({
                'success': False,
                'message': "hatolik: Bu mahsulot allaqachon Dislike qo'shilgan."
            })

        return Response({'success': True, 'message': 'Dislike qo‘shildi'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Dislike item removed successfully.'
        })


