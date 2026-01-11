from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .tasks import send_price_notifications,  notify_followers_new_product
from django.db.models import F , Prefetch, Count ,Q
from rest_framework import viewsets
from rest_framework import status
from django.db import transaction
from decimal import Decimal
from .serializers import *
from .decorators import *
from .models import *
P_NUM = 20

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    http_method_names = ['post', 'put', 'delete', 'get'] 
    
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsStaff()]
    
    def list(self, request):
        pk = request.GET.get('id')
        category  = Category.objects.get(id=pk)
        sub_categories = (
        category.children
        .filter(level=2)
        .prefetch_related(
            Prefetch(
                'children',
                queryset=Category.objects.filter(level=3),
                to_attr='prefetched_sub_subs'
            )
        )
    )

        serializer = SubCategorySerializer(sub_categories, many=True)
        
        return Response({
            'success': True,
            'sub_categories': serializer.data
            
    
        })

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        img = data.get('img')
        category_id = data.get('category')
        
        category = Category.objects.create(name=name)
        if img:
            category.img = img  
        if category_id:
            category.category = Category.objects.get(id=category_id)
        category.save()
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


class ModelViewSet(viewsets.ModelViewSet):
    serializer_class = ModelSerializer
    http_method_names = ['post', 'put', 'delete'] 
    # permission_classes = [IsStaff]
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [AllowAny()]
        return [AllowAny()]
        # return [IsStaff()]

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category')
        queryset = Model.objects.filter(category_id=category).select_related('category')
        serializer = ModelSerializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })
    def retrieve(self, request, *args, **kwargs):
        try:
            model = Model.objects.select_related('category').get(id=kwargs['pk'])
            serializer = ModelSerializer(model, many=False)
            return Response({
                "success": True,
                "data": serializer.data
            })
        except Model.DoesNotExist:
            return Response({
                "success": False,
                "error": "Model not found"
            }, status=404)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        category_id = data.get('category')

        model = Model.objects.create(name=name, category_id=category_id)
        return Response({
            'success': True,
            'data': ModelSerializer(model, many=False).data
        })
    def update(self, request, *args, **kwargs):
        data = request.data 
        id = kwargs['pk']
        name = data.get('name')
        category_id = data.get('category')
     
        try:
            model = Model.objects.get(id=id)
            model.name = name
            model.category_id = category_id
            model.save()
    
            return Response({
                "success": True,
                'data': ModelSerializer(model, many = False).data
            })
        except:
            return Response({
                "success": False
            })
    def destroy(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            model = Model.objects.get(id=id)
            model.delete()
            
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


class ProductViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        image_prefetch = Prefetch(
            'image',
            queryset=Image.objects.only('id', 'image'),
            to_attr='prefetched_images'
        )

        return (
            Product.objects
            .filter(is_active=True)
            .select_related('category', 'region', 'user', 'model')
            .prefetch_related(image_prefetch)
            
            .annotate(
                like_count=Count('likes', distinct=True),
                dislike_count=Count('dislikes', distinct=True)
            )
    )
     
    @action(methods=['get'], detail=False)
    def search(self, request):
        queryset = self.get_queryset()
        q = request.query_params.get('q', '')

        if q:
            queryset = queryset.filter(Q(title__icontains=q) |
                                       Q(description__icontains=q)|
                                       Q(model__name__icontains=q)| 
                                       Q(category__name__icontains=q))

        page = PageNumberPagination()
        page.page_size = P_NUM
        page_qs = page.paginate_queryset(queryset, request)

        serializer = ProductSerializer(
            page_qs, many=True, context={'request': request}
        )
        return page.get_paginated_response(serializer.data)
       
    def list(self, request):
        queryset = self.get_queryset()
        filters = {}

        qp = request.query_params

        if title := qp.get("title"):
            filters["title__icontains"] = title

        if sold := qp.get("sold"):
            if sold in ["sold", "not_sold"]:
                filters["sold"] = sold

        if exchange := qp.get("exchange"):
            if exchange in ["True", "False"]:
                filters["exchange"] = exchange == "True"

        if trade := qp.get("trade"):
            if trade in ["True", "False"]:
                filters["trade"] = trade == "True"

        if category_name := qp.get("category_name"):
            filters["category__name__icontains"] = category_name

        if user := qp.get("user"):
            filters["user_id"] = user

        if region := qp.get("region"):
            filters["region_id"] = region

        if category := qp.get("category"):
            filters["category_id"] = category

        if price := qp.get("price"):
            try:
                price = int(price)
                filters["price__gte"] = price - 50000
                filters["price__lte"] = price + 50000
            except ValueError:
                pass

        queryset = queryset.filter(**filters)

        page = PageNumberPagination()
        page.page_size = P_NUM
        page_qs = page.paginate_queryset(queryset, request)

        serializer = ProductSerializer(
            page_qs, many=True, context={'request': request}
        )
        return page.get_paginated_response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        product = self.get_queryset().filter(id=kwargs['pk']).first()
        if not product:
            return Response({"detail": "Product not found"}, status=404)

        # atomic view count
        Product.objects.filter(id=product.id).update(
            views_count=F('views_count') + 1
        )
        product.views_count += 1  # refresh qilmasdan

        related_products = (
            self.get_queryset()
            .filter(category=product.category)
            .exclude(id=product.id)
            .order_by('-created_at')[:20]
        )

        return Response({
            'product': ProductDetailSerializer(
                product, context={'request': request}
            ).data,
            'products': ProductSerializer(
                related_products, many=True, context={'request': request}
            ).data
        })

    def update(self, request, *args, **kwargs):
        data = request.data
        id = kwargs['pk']
        title = data.get('title')
        price = data.get('price')
        region = data.get('region')
        category = data.get('category')
        model = data.get('model')
        description = data.get('description')
        address = data.get('address')
        phone_number = data.get('phone_number')

        # try:
        product = Product.objects.select_related('category', 'region', 'user').get(id=id)
        if request.user.id != product.user.id:
            return Response({
                "success": False,
                "permissions": False
            })
        if title:
            product.title = title

        if price is not None:
            old_price = product.price
            price = Decimal(price)

            if price != old_price:
                product.price = price
                product.save(update_fields=['price'])

                send_price_notifications.delay(
                    product.id,
                    str(old_price),
                    str(price)
                )
        if region:
            product.region_id = region
        if category:
            product.category_id = category
        if model:
            product.model_id = model
        if description:
            product.description = description
        if address:
            product.address = address
        if phone_number:
            product.phone_number = phone_number
        product.save()

        return Response({
            "success": True,
            'data': ProductSerializer(product, many=False, context={'request': request}).data
        })

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        product = Product.objects.get(id=pk)
        if request.user.id != product.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        if product.sold == 'sold':
            product.sold = 'not_sold'
            # product.is_active = True
        else:
            product.sold = 'sold'
            # product.is_active = False
        product.save()
        return Response({
            'success': True,
            'data': ProductSerializer(product, many = False, context={'request': request}).data
        })
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        product = self.get_object()
         
        if request.user.id != product.user.id:
            return Response({
                'success':False,
                'permissions':False
            })
        count =  product.image.all().count()
        if count >= 5:
          return Response({
                'success':False,
                'limit':'5 ta rasmgacha yuklash mumkin',
                'count':count
            }) 
        image = request.FILES.get('image')
        if image.split('.')[-1].lower() not in ['jpg','jpeg','png','webp']:
            return Response({
                "success": False,
                "error": "Rasmlar faqat jpg, jpeg, png, webp formatlarida bo‘lishi kerak"
            })
        if image:
            img = Image.objects.create(image=image, user=request.user) 
            product.image.add(img)
            return Response({
                'success': True,
                'data': ProductSerializer(product, many = False, context={'request': request}).data
            })
        return Response({
            'success': False,
            'error': 'Image not provided'
        })
    
    def create(self, request, *args, **kwargs):
        try:
            images = request.FILES.getlist('images')
            if len(images) > 5:
                return Response({
                    "success": False,
                    "error": "5 tadan ko‘p rasm yuklab bo‘lmaydi"
                })

            ALLOWED_EXT = ['jpg', 'jpeg', 'png', 'webp']

            for i in images:
                ext = i.name.split('.')[-1].lower()
                if ext not in ALLOWED_EXT:
                    return Response({
                        "success": False,
                        "error": "Rasmlar faqat jpg, jpeg, png, webp formatlarida bo‘lishi kerak"
                    }, status=400)
            
            user = request.user
            data = request.data
            title = data.get('title') # bor 
            price = data.get('price') # bor
            region = data.get('region') # bor
            category =data.get('category') # bor
            description =data.get('description') # bor
            address =data.get('address') # bor
            model =data.get('model') # yo'q
            phone_number =data.get('phone_number') # bor
            money_type =data.get('money_type') # bor
            dostafca = data.get('dostafca') # bor
            trade =data.get('trade') # bor
            exchange =data.get('exchange') # bor
            lan = data.get('lan')
            lat = data.get('lat')
            
            product = Product.objects.create(
                title= title,
                price=price,
                region_id=region,
                category_id=category,
                description= description,
                address=address,
                user=user,
                phone_number=phone_number,
                money_type=money_type,
                trade=trade,
                dostafca=dostafca,
                exchange=exchange,
                lan=lan,
                lat=lat,
                is_active=False
                
            )
            if model:
                product.model_id = model
            product.save()
            img = Image.objects.bulk_create([Image(image=image, user=request.user) for image in images])
            product.image.set(img)
            notify_followers_new_product.delay(product.id)
            return Response(ProductSerializer(product, context={'request': request}).data)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": str(e)
                }   
            )
    
    def destroy(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            if product.user != request.user:
                return Response({
                    "success": False,
                    "permissions": False
                })
            for i in product.image.all():
                i.image.delete(save=False)
                i.delete()
                
              
            product.delete()
            return Response({
                "success": True
            })
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            })

    
    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def my_product(self,request):
        product = Product.objects.filter(user=request.user).order_by('-id')

        return Response(
           ProductSerializer(product, many=True).data
        )

    @action(methods=['get'], detail=False, permission_classes=[IsStaff])
    def product_false(request):
        filters = {"is_active": False}

        region = request.query_params.get("region")
        if region:
            filters["region_id"] = region
        
        category = request.query_params.get('category')
        if category:
            filters['category'] = category

        user = request.query_params.get('user')
        if user:
            filters['user_id'] = user

        price = request.query_params.get('price')
        if price:
            try:
                price = int(price)
                filters['price__gte'] = price - 50000   # masalan 25 mingdan past 20 ming
                filters['price__lte'] = price + 50000  # yuqoriga 30 ming
            except : pass
        all_data = Product.objects.filter(**filters).select_related('region','category','model','user',).order_by("-id")
        # Paginatsiya
        serializers = ProductSerializer(all_data, many=True, context={'request': request})
        paginator = PageNumberPagination()
        paginator.page_size = 5 # har bir sahifada 20 tadan
        result_page = paginator.paginate_queryset(serializers.data, request)

        return paginator.get_paginated_response(result_page)
        

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer 
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        
        return Response({
            "success": True,
            "data": LikeSerializer(self.get_queryset(), many=True).data
        })


    
    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related("user", "product").order_by('-id')

    def create(self, request, *args, **kwargs):
        data = request.data# masalan: "job"
        object_id = data.get('object_id')

        if Dislike.objects.filter(user=request.user, product_id=object_id).exists():
            return Response({'success': False, 'message': 'Avval dislike bosilgan'}, status=400)
        
        favorite, created = Like.objects.get_or_create(
            user=request.user,
            product_id=object_id
        )

        if created == False:
            favorite.delete()
            return Response({
                'success': False,
                'message': "like o'chirildi:"
            })

        return Response({'success': True, 'message': 'Like qo‘shildi'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Like o‘chirildi'
        })


class DislikeViewSet(viewsets.ModelViewSet):
    serializer_class = DislikeSerializer 
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        
        return Response({
            "success": True,
            "data": DislikeSerializer(self.get_queryset(), many=True).data
        })


    
    def get_queryset(self):
        return Dislike.objects.filter(user=self.request.user).select_related("user", "product").order_by('-id')

    def create(self, request, *args, **kwargs):
        data = request.data
        object_id = data.get('object_id')


        if Like.objects.filter(user=request.user, product_id=object_id).exists():
            return Response({'success': False, 'message': 'Avval like bosilgan'}, status=400)
        
        favorite, created = Dislike.objects.get_or_create(
            user=request.user,
            product_id=object_id
        )

        if created == False:
            favorite.delete()
            return Response({
                'success': False,
                'message': "dislike o'chirildi:"
            })

        return Response({'success': True, 'message': 'Dislike qo‘shildi'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Dislike o‘chirildi'
        })


class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class =  ComplaintSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self,request):
        if request.user.is_staff:
            complaint= Complaint.objects.filter(is_saw=False).order_by('-id')
            serializer = ComplaintSerializer(complaint, many=True)
            return Response(serializer.data)
        complaint= Complaint.objects.filter(user=request.user).order_by('-id')
        serializer = ComplaintSerializer(complaint, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        complaint= Complaint.objects.get(id=kwargs['pk'])
        if request.user.is_staff or complaint.user.id == request.user.id:
            serializers = (ComplaintSerializer(complaint, many= False))
            return Response(serializers.data)
        return Response({'success': False})
    
    def create(self, request, *args, **kwargs ):
        data = request.data
        user = request.user
        product_id = data['object_id']
        text = data['text']

        complaint, created = Complaint.objects.get_or_create(
            user=user,
            product_id=product_id
        )
        complaint.text = text
        complaint.save()
        serializer = ComplaintSerializer(complaint, many= False,context={'request':request})
        return Response(serializer.data)
    
    @action(methods=['get'],detail=False)
    def is_saw_true(self, request, *args, **kwargs):
        if request.user.is_staff:
            complaint= Complaint.objects.filter(is_saw=True).order_by('-id')
            serializer = ComplaintSerializer(complaint, many=True, context={'request':request})
            return Response(serializer.data)
        return Response({'success': False})
    
    @action(methods=['post'],detail=True)
    def is_saw_(self, request, *args, **kwargs):
        if request.user.is_staff:
            complaint= Complaint.objects.get(id=kwargs['pk'])
            complaint.is_saw = True
            complaint.save()
            return Response({
                'success': True
            })
        return Response({
                'success': False
            })
    def destroy(self, request, *args, **kwargs):
        complaint= Complaint.objects.get(id=kwargs['pk'])
        if request.user.is_staff or complaint.user.id == request.user.id:
            complaint.delete()
            return Response({
                'success': True,
                'message': 'Complaint o‘chirildi'
            })
        return Response({
            'success': False,
            'message': 'Complaint o‘chirib bo‘lmaydi'
        })
    