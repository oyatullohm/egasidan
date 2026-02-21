from rest_framework import serializers
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        
class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    models = ModelSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id','img','category_name','name','level','category','models']
        # depth = 1

    def get_img(self, obj):
        request = self.context.get('request')

        if obj.img and hasattr(obj.img, 'url'):
            if request:
                return request.build_absolute_uri(obj.img.url)
            return obj.img.url
        return None
        
    def get_category_name(self, obj):
        names = []
        category = obj.category

        while category:
            names.append(category.name)
            category = category.category

        return "  ".join(names) if names else None

class CategoryIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','level','category']

class SubCategorySerializer(serializers.ModelSerializer):
    sub_sub_category = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'level', 'sub_sub_category']

    
    def get_sub_sub_category(self, obj):
        sub_subs = getattr(obj, 'prefetched_sub_subs', [])
        return CategoryIDSerializer(sub_subs, many=True).data

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, read_only=True)
    model = ModelSerializer( read_only=True)
    category = CategorySerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    dislike_count = serializers.IntegerField(read_only=True)
    i_like = serializers.BooleanField(read_only=True)
    i_dislike = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


    # def get_image(self, obj):
    #     images = getattr(obj, 'prefetched_images', [])
    #     if images:
    #         request = self.context.get('request')
    #         return request.build_absolute_uri(images[0].image.url)
    #     return None
    
    def get_model(self, obj):
        return obj.model.name if obj.model else None

class PriceWatchSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = PriceWatch
        fields = ('id', 'user', 'product', 'last_price', 
                  'created_at')

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ['id','image','product']

    def get_product(self, obj):
        product = Product.objects.filter(image_id=obj.id).first()
        return ProductSerializer(product).data
    
    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return f"{obj.image.url}"
        return None

class ComplaintSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = [ 'id','created_at','text','product','user','is_saw'
                  ]
    
    def get_product(self,obj):
        request = self.context.get('request')
        return ProductSerializer(obj.product, context={'request': request}).data

class ProductDetailSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    like = serializers.IntegerField(source='like_count', read_only=True)
    dislike = serializers.IntegerField(source='dislike_count', read_only=True)
    image = serializers.SerializerMethodField()  # Prefetch uchun
    i_like = serializers.SerializerMethodField()
    i_dislike = serializers.SerializerMethodField()
    is_watching = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = "__all__"

    def get_is_watching(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PriceWatch.objects.filter(
                user=request.user,
                product=obj
            ).exists()
        return False
    def get_i_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(
                user=request.user,
                product=obj
            ).exists()
        return False
    def get_i_dislike(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Dislike.objects.filter(
                user=request.user,
                product=obj
            ).exists()
        return False
    
    def get_image(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'prefetched_images'):
            return [
                {
                    "id": img.id,
                    "image": request.build_absolute_uri(img.image.url) if request else img.image.url
                }
                for img in obj.prefetched_images
            ]
        return []

class DislikeSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Dislike
        fields = '__all__'
        
class LikeSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Like
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Complaint
        fields = [ 'id','created_at','text','product','user','type','is_saw'
                  ]
    
    # def get_product(self,obj):
    #     request = self.context.get('request')
    #     if obj.product:
    #         return ProductSerializer(obj.product, context={'request': request}).data
    #     return ''