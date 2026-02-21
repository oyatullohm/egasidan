# from .tasks import send_price_notifications,  notify_followers_new_product
from django.db.models import F , Prefetch, Count ,Q, Exists, OuterRef, Value, Subquery , BooleanField
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .utils import send_push_notification
from rest_framework import viewsets
from rest_framework import status
from django.db import transaction
from decimal import Decimal
from .serializers import *
from .decorators import *
from .models import *
P_NUM = 10

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
        if self.action in ['list', 'retrieve','get','search']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        image_prefetch = Prefetch(
            'image',
            queryset=Image.objects.only('id', 'image'),
            to_attr='prefetched_images'
        )

        queryset = (
            Product.objects
            .select_related('category', 'category__category', 'region', 'user', 'model')
            .prefetch_related(image_prefetch,'image', 'category__models')
            .annotate(
                like_count=Count('likes', distinct=True),
                dislike_count=Count('dislikes', distinct=True),
            )
        )

        if user.is_authenticated:
            queryset = queryset.annotate(
                i_like=Exists(
                    Like.objects.filter(
                        user=user,
                        product=OuterRef('pk')
                    )
                ),
                i_dislike=Exists(
                    Dislike.objects.filter(
                        user=user,
                        product=OuterRef('pk')
                    )
                )
            )
        else:
            queryset = queryset.annotate(
                i_like=Exists(Like.objects.none()),
                i_dislike=Exists(Dislike.objects.none())
            )

        return queryset

    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def search(self, request):
        try:


            queryset = self.get_queryset()
            filters = {}
            qp = request.query_params

            # ========= SIMPLE FIELDS =========

            if condition := qp.get("condition"):
                condition = condition.strip()
                if condition:
                    filters["condition__icontains"] = condition

            if contact_name := qp.get("contact_name"):
                contact_name = contact_name.strip()
                if contact_name:
                    filters["contact_name__icontains"] = contact_name

            if sold := qp.get("sold"):
                if sold in ["sold", "not_sold"]:
                    filters["sold"] = sold

            if exchange := qp.get("exchange"):
                if exchange.lower() in ["true", "false"]:
                    filters["exchange"] = exchange.lower() == "true"

            if trade := qp.get("trade"):
                if trade.lower() in ["true", "false"]:
                    filters["trade"] = trade.lower() == "true"

            if user := qp.get("user"):
                filters["user_id"] = user

            if region := qp.get("region"):
                filters["region_id"] = region

            if category := qp.get("category"):
                filters["category_id"] = category

            if model := qp.get("model"):
                filters["model_id"] = model

            # ========= PRICE RANGE =========

            if price_from := qp.get("from"):
                try:
                    price_from = int(price_from)
                    filters["price__gte"] = price_from
                except ValueError:
                    pass

            # UP TO price
            if price_to := qp.get("up_to"):
                try:
                    price_to = int(price_to)
                    filters["price__lte"] = price_to
                except ValueError:
                    pass

            # ========= GLOBAL SEARCH =========

            if q := qp.get("q"):
                q = q.strip()
                if q:
                    queryset = queryset.filter(
                        Q(title__icontains=q) |
                        Q(description__icontains=q) |
                        Q(model__name__icontains=q) |
                        Q(category__name__icontains=q)
                    )
            queryset = queryset.filter(**filters)


            page = PageNumberPagination()
            page.page_size = P_NUM
            page_qs = page.paginate_queryset(queryset, request)

            serializer = ProductSerializer(
                page_qs, many=True, context={'request': request}
            )
            return page.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)
        }, status=400)  
    
    def list(self, request):
        try:
            queryset = self.get_queryset()

            page = PageNumberPagination()
            page.page_size = P_NUM
            page_qs = page.paginate_queryset(queryset, request)

            serializer = ProductSerializer(
                page_qs, many=True, context={'request': request}
            )
            return page.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)
    
    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def status(self, request):
        try:
            queryset = self.get_queryset()

            queryset = queryset.filter(is_status=True)

            page = PageNumberPagination()
            page.page_size = P_NUM
            page_qs = page.paginate_queryset(queryset, request)

            serializer = ProductSerializer(
                page_qs, many=True, context={'request': request}
            )
            return page.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)
             
    def retrieve(self, request, *args, **kwargs):
        # Product topish
        product = self.get_queryset().filter(id=kwargs['pk']).first()
        if not product:
            return Response({"detail": "Product not found"}, status=404)

        # Atomic view count update
        Product.objects.filter(id=product.id).update(
            views_count=F('views_count') + 1
        )
        product.views_count += 1  # memoryda update

        # related products (shu category dan)
        related_products = (
            self.get_queryset()
            .filter(category=product.category)
            .exclude(id=product.id)
            .order_by('-created_at')[:20]
        )
        if request.user.is_authenticated:
            RecentlyViewed.objects.update_or_create(
            user=request.user,
            product=product
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
        try:
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
            condition = data.get('condition')
            contact_name = data.get('contact_name')
            trade = data.get('trade')
            exchange = data.get('exchange')
            dostafca = data.get('dostafca')
            # try:
            product = Product.objects.select_related('category', 'region', 'user').get(id=id)
            if request.user.id != product.user.id:
                return Response({
                    "success": False,
                    "permissions": False
                })
            if trade is not None:
                product.trade = trade
            if dostafca is not None:
                product.dostafca = dostafca

            if exchange is not None:
                product.exchange = exchange
                        
            if title:
                product.title = title
            
            if contact_name:
                product.contact_name = contact_name
            
            if condition:
                product.condition = condition
            
            
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
            if price is not None:
                old_price = product.price
                price = Decimal(price)

                if price != old_price:
                    product.price = price
                    product.save(update_fields=['price'])
                    try:
                        PriceWatch.objects.filter(product=product).update(last_price=price) 
                    except:pass
                    # send_price_notifications.delay(
                    #     product.id,
                    #     str(old_price),
                    #     str(price)
                    # )
            product.save()
            return Response({
                "success": True,
                'data': ProductSerializer(product, many=False, context={'request': request}).data
            })
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def sold(self, request, pk=None):
        try:
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
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
    
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_img(self, request, pk=None):
        try:
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
                        
                    }, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE) 
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
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
    
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
            contact_name = data.get('contact_name') # bor
            condition = data.get('condition') # bor
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
                is_active=False,
                contact_name=contact_name,
                condition=condition
                
                
            )
            if model:
                product.model_id = model
            product.save()
            for i in  images:
                img = Image.objects.create(image=i,user=request.user)
                product.image.add(img)
            # notify_followers_new_product.delay(product.id)
            return Response(ProductSerializer(product, context={'request': request}).data)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": str(e)
                }, status=400 
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
            }, status=400)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def my_product(self,request):
        try:
            product = self.get_queryset().filter(user=request.user).order_by('-id')
            return Response(
            ProductSerializer(product, many=True, context={'request': request}).data
            )
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  

    @action(methods=['get'], detail=False, permission_classes=[IsStaff])
    def product_false(request):
        try:
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
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)

class RecentlyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user

        image_prefetch = Prefetch(
            'image',
            queryset=Image.objects.only('id', 'image'),
            to_attr='prefetched_images'
        )

        queryset = (
            Product.objects
            # 🔥 FAQAT recently ko‘rilgan productlar
            .filter(recentlyviewed__user=user)
            .select_related(
                'category',
                'category__category',
                'region',
                'user',
                'model'
            )
            .prefetch_related(
                image_prefetch,
                'category__models'
            )
            .annotate(
                like_count=Count('likes', distinct=True),
                dislike_count=Count('dislikes', distinct=True),
                i_like=Exists(
                    Like.objects.filter(
                        user=user,
                        product=OuterRef('pk')
                    )
                ),
                i_dislike=Exists(
                    Dislike.objects.filter(
                        user=user,
                        product=OuterRef('pk')
                    )
                ),
                last_viewed_at=Subquery(
                    RecentlyViewed.objects.filter(
                        user=user,
                        product=OuterRef('pk')
                    ).values('viewed_at')[:1]
                )
            )
            .order_by('-last_viewed_at')
            .distinct()
        )

        return queryset

    
    def list(self, request):
        try:
            queryset = self.get_queryset()
            page = PageNumberPagination()
            page.page_size = P_NUM
            page_qs = page.paginate_queryset(queryset, request)

            serializer = ProductSerializer(
                page_qs, many=True, context={'request': request}
            )
            return page.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer 
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            page = PageNumberPagination()
            page.page_size = P_NUM  # masalan 10 yoki settings dan oling

            page_qs = page.paginate_queryset(queryset, request)

            serializer = self.get_serializer(page_qs, many=True)

            return page.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
 
    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related("user", "product")\
            .prefetch_related(
                'product__image',
                'product__category',
                'product__model',
                'product__region',
                'product__category__models',
                'product__user'
                
                
            ).order_by('-id')

    def create(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'success': True,
                'message': 'Like o‘chirildi'
            })
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
    
class DislikeViewSet(viewsets.ModelViewSet):
    serializer_class = DislikeSerializer 
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            page = PageNumberPagination()
            page.page_size = P_NUM  # masalan 10 yoki settings dan oling

            page_qs = page.paginate_queryset(queryset, request)

            serializer = self.get_serializer(page_qs, many=True)

            return page.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  

    def get_queryset(self):
        return Dislike.objects.filter(user=self.request.user).select_related("user", "product")\
              .prefetch_related(
                'product__image',
                'product__category',
                'product__model',
                'product__region',
                'product__category__models',
                'product__user'
                
                
            ).order_by('-id')

    def create(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'success': True,
                'message': 'Dislike o‘chirildi'
            })
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  

class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class =  ComplaintSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self,request):
        try:
            if request.user.is_staff:
                complaint= Complaint.objects.filter(is_saw=False).select_related('user','product')\
                .prefetch_related(
                'product__image',
                'product__category',
                'product__model',
                'product__region',
                'product__category__models',
                'product__user'
                
                
            ).order_by('-id')
                serializer = ComplaintSerializer(complaint, many=True)
                return Response(serializer.data)
            complaint= Complaint.objects.filter(user=request.user).select_related('user','product')\
                .prefetch_related(
                'product__image',
                'product__category',
                'product__model',
                'product__region',
                'product__category__models',
                'product__user'
                
                
            ).order_by('-id')
            page = PageNumberPagination()
            page.page_size = P_NUM  
            page_qs = page.paginate_queryset(complaint, request)
            serializer = ComplaintSerializer(page_qs, many=True, context={'request':request})
            return page.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)

    def retrieve(self, request, *args, **kwargs):
        try:
            complaint= Complaint.objects.get(id=kwargs['pk'])
            if request.user.is_staff or complaint.user.id == request.user.id:
                serializers = (ComplaintSerializer(complaint, many= False))
                return Response(serializers.data)
            return Response({'success': False})
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
    
    def create(self, request, *args, **kwargs ):
        try:
            data = request.data
            user = request.user
            product_id = data.get('object_id')
            text = data.get('text')
            type = data.get('type')

            complaint = Complaint.objects.create(
                user=user,
                type=type
                
            )
            try:
                product = Product.objects.get(id= product_id)
                complaint.product = product
                complaint.save()
            except:
                pass
                
            complaint.text = text
            complaint.save()
            serializer = ComplaintSerializer(complaint, many= False,context={'request':request})
            return Response(serializer.data)
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
        
    @action(methods=['get'],detail=False)
    def is_saw_true(self, request, *args, **kwargs):
        try:
            if request.user.is_staff:
                complaint= Complaint.objects.filter(is_saw=True).order_by('-id')
                serializer = ComplaintSerializer(complaint, many=True, context={'request':request})
                return Response(serializer.data)
            return Response({'success': False})
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
    
    @action(methods=['post'],detail=True)
    def is_saw_(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  
    
    def destroy(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)  

class PriceWatchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PriceWatchSerializer
    
    def get_queryset(self):
        return PriceWatch.objects.filter(user=self.request.user)\
            .select_related('user', 'product')\
            .prefetch_related('product__image', 'product__category', 'product__model',
                              'product__region', 'product__user','product__category__models' )\
            .order_by('-id')    
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = PageNumberPagination()
            page.page_size = P_NUM
            page_qs = page.paginate_queryset(queryset, request)

            serializer = PriceWatchSerializer(
                page_qs, many=True, context={'request': request}
            )
            return page.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)
    
    def create(self, request):
        try:
            product_id = request.data.get('product_id')

            product = Product.objects.get(id=product_id)

            pricewatch, created = PriceWatch.objects.get_or_create(
                user=request.user,
                product=product,
            )
            pricewatch.last_price=product.price
            pricewatch.save()

            serializer = PriceWatchSerializer(pricewatch)
            return Response(serializer.data)
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400) 
    
    def destroy(self, request, *args, **kwargs):
        try:
            priwatch = PriceWatch.objects.get(id=kwargs['pk'])
            if priwatch.user == request.user:
                priwatch.delete()
            
            
                return Response({
                'success': True,
                'message': 'PriceWatch o‘chirildi'
                }, status=204)
            return Response({
                'success': True,
                'message': 'permission none'
                }, status=204) 
            
        except Exception as e:
            return Response({
            "success": False,
            "error": str(e)  # aynan xato matnini qaytaradi
        }, status=400)
            