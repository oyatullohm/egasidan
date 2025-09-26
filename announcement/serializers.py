from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_img(self, obj):
        if obj.img and hasattr(obj.img, 'url'):
            return f"{obj.img.url}"
        return None


class SubCategorySerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = SubCategory
        fields = '__all__'
        # depth = True
    
    def get_img(self, obj):
        if obj.img and hasattr(obj.img, 'url'):
            return f"{obj.img.url}"
        return None
    
    
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

        
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ModellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modell
        fields = '__all__'


class VehiclelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id','description', 'price', 'old_price','condition','image_urls'
            ]


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_type = serializers.ChoiceField(choices=Vehicle.VEHICLE_TYPES)
    fuel_type = serializers.ChoiceField(choices=Vehicle.FUEL_TYPES)
    transmission = serializers.ChoiceField(choices=Vehicle.TRANSMISSION_TYPES)
    content_type = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'user','description','price','condition','address',
            'produced','phone_number','is_active','views_count',
            'created_at','vehicle_type','brand','mileage',
            'engine_size','fuel_type','transmission','color','category',
            'district','model','image_urls','sold','content_type',
            'likes_count','dislikes_count', 'is_liked', 'is_disliked'
            
        ]
        # depth = True1/
    
    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).id

    def get_likes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Favorite.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
        
    def get_dislikes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Dislike.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Favorite.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False

    
    def get_is_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Dislike.objects.filter(
                content_type=content_type,
                object_id=obj.id,
                user=request.user
            ).exists()
        return False
    

class PropertylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id','description', 'price', 'old_price','condition','image_urls'
            ]

class PropertySerializer(serializers.ModelSerializer):
    property_type= serializers.ChoiceField(choices=Property.PROPERTY_TYPES)
    content_type = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = [
            'id', 'description', 'price', 'old_price','condition', 'address',
            'produced','phone_number', 'is_active', 'created_at',
            'property_type', 'category', 'district','image_urls',
            'views_count', 'sold',"area","rooms",'content_type',
            'likes_count','dislikes_count', 'is_liked', 'is_disliked'
        ]
        depth = True
    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).id

    def get_likes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Favorite.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
        
    def get_dislikes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Dislike.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Favorite.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False

    
    def get_is_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Dislike.objects.filter(
                content_type=content_type,
                object_id=obj.id,
                user=request.user
            ).exists()
        return False


class ElectronicslistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Electronics
        fields = [
            'id','description', 'price', 'old_price','condition','image_urls'
            ]

class ElectronicsSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    electronic_type= serializers.ChoiceField(choices=Electronics.ELECTRONIC_TYPES)
    class Meta:
        model = Electronics
        fields = [
            'id','description', 'price', 'old_price','condition', 'address',
            'produced','phone_number', 'is_active', 'created_at',
            'category', 'district','image_urls',
            'views_count', 'sold','electronic_type','brand','model',
            'warranty','warranty_months', 'content_type',
            'likes_count','dislikes_count', 'is_liked', 'is_disliked'
        ]
    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).id
    def get_likes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Favorite.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
        
    def get_dislikes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Dislike.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Favorite.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False

    
    def get_is_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Dislike.objects.filter(
                content_type=content_type,
                object_id=obj.id,
                user=request.user
            ).exists()
        return False

    
class JoblistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id','description', 'price', 'old_price','condition','image_urls'
            ]

class JobSerializer(serializers.ModelSerializer):
    job_type= serializers.ChoiceField(choices=Job.JOB_TYPES)
    content_type = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    class Meta:
        model = Job
        fields = [
            'id','description', 'price', 'old_price','condition', 'address',
            'produced','phone_number', 'is_active', 'created_at',
            'category', 'district','image_urls','telegram',
            'views_count', 'sold','job_type','company',
            'application_deadline','remote_work','content_type',
            'likes_count','dislikes_count', 'is_liked', 'is_disliked'
        ]
    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).id

    def get_likes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Favorite.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
        
    def get_dislikes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Dislike.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Favorite.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False

    
    def get_is_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Dislike.objects.filter(
                content_type=content_type,
                object_id=obj.id,
                user=request.user
            ).exists()
        return False
    
    
class ServicelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id','description', 'price', 'old_price','condition','image_urls'
            ]

class ServiceSerializer(serializers.ModelSerializer):
    service_type= serializers.ChoiceField(choices=Service.SERVICE_TYPES)
    content_type = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    class Meta:
        model = Service
        fields = [
            'id','description', 'price', 'old_price','condition', 'address',
            'produced','phone_number', 'is_active', 'created_at',
            'category', 'district','image_urls',
            'views_count', 'sold','service_type','experience_years',
            'availability','content_type',
            'likes_count','dislikes_count', 'is_liked', 'is_disliked'
        ]
    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).id

    def get_likes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Favorite.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
        
    def get_dislikes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Dislike.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Favorite.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False

    
    def get_is_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Dislike.objects.filter(
                content_type=content_type,
                object_id=obj.id,
                user=request.user
            ).exists()
        return False


class HouseholdItemslistSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdItems
        fields = [
            'id','description', 'price', 'old_price','condition','image_urls'
            ]

class HouseholdItemsSerializer(serializers.ModelSerializer):
    hourse_type= serializers.ChoiceField(choices=HouseholdItems.HOUSEHOLD_TYPES)
    content_type = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    
    class Meta:
        model = HouseholdItems
        fields = [
             'id','description', 'price', 'old_price','condition', 'address',
            'produced','phone_number', 'is_active', 'created_at',
            'category', 'district','image_urls',
            'views_count', 'sold','hourse_type','model','experience_years',
            'content_type',
            'likes_count','dislikes_count', 'is_liked', 'is_disliked'
        ]
        
    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).id
    
    def get_likes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Favorite.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
        
    def get_dislikes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Dislike.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Favorite.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False

    
    def get_is_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Dislike.objects.filter(
                content_type=content_type,
                object_id=obj.id,
                user=request.user
            ).exists()
        return False

  
class SportingGoodslistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportingGoods
        fields = [
            'id','description', 'price', 'old_price','condition','image_urls'
            ]

class SportingGoodsSerializer(serializers.ModelSerializer):
    sport_type= serializers.ChoiceField(choices=SportingGoods.SPORT_TYPE)
    content_type = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    
    class Meta:
        model = SportingGoods
        fields = [
            'id','description', 'price', 'old_price','condition', 'address',
            'produced','phone_number', 'is_active', 'created_at',
            'category', 'district','image_urls',
            'views_count', 'sold','sport_type','brand','model','content_type',
            'likes_count','dislikes_count', 'is_liked', 'is_disliked'
        ]
    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).id

    def get_likes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Favorite.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
        
    def get_dislikes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Dislike.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Favorite.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False

    
    def get_is_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Dislike.objects.filter(
                content_type=content_type,
                object_id=obj.id,
                user=request.user
            ).exists()
        return False

class PetlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            'id','description', 'price', 'old_price','condition','image_urls'
            ]

class PetSerializer(serializers.ModelSerializer):
    animal_type= serializers.ChoiceField(choices=Pet.ANIMAL_TYPE)
    content_type = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    class Meta:
        model = Pet
        fields = [
            'id','description', 'price', 'old_price','condition', 'address',
            'produced','phone_number', 'is_active', 'created_at',
            'category', 'district','image_urls',
            'views_count', 'sold','animal_type','breed','age','content_type',
            'likes_count','dislikes_count', 'is_liked', 'is_disliked'
        ]


    
    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).id

    def get_likes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Favorite.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
        
    def get_dislikes_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Dislike.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Favorite.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False

    
    def get_is_disliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(obj)
            return Dislike.objects.filter(
                content_type=content_type,
                object_id=obj.id,
                user=request.user
            ).exists()
        return False


PRODUCT_SERIALIZERS = {
            Job: JoblistSerializer,
            Vehicle: VehiclelistSerializer,
            Property: PropertylistSerializer,
            Electronics: ElectronicslistSerializer,
            Service: ServicelistSerializer,
            HouseholdItems: HouseholdItemslistSerializer,
            SportingGoods: SportingGoodslistSerializer,
            Pet: PetlistSerializer,
            }


class FavoriteSerializer(serializers.ModelSerializer):
    # content_type = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = [  'id','object_id',
                  'created_at','product'
                  ]
  
    def get_product(self, obj):
        product = obj.product
        serializer_class = PRODUCT_SERIALIZERS.get(type(product))
        if serializer_class:
            return serializer_class(product).data
        return None
    

class DislikeSerializer(serializers.ModelSerializer):
    # content_type = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Dislike
        fields = [  'id','object_id',
                  'created_at','product'
                  ]
  
    def get_product(self, obj):
        product = obj.product
        serializer_class = PRODUCT_SERIALIZERS.get(type(product))
        if serializer_class:
            return serializer_class(product).data
        return None