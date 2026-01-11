from rest_framework import serializers
from .models import *

class   ModelSerializer(serializers.ModelSerializer):
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
        if obj.img and hasattr(obj.img, 'url'):
            return f"{obj.img.url}"
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
    image = serializers.SerializerMethodField()
    model = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        images = getattr(obj, 'prefetched_images', [])
        if images:
            request = self.context.get('request')
            return request.build_absolute_uri(images[0].image.url)
        return None
    
    def get_model(self, obj):
        return obj.model.name if obj.model else None

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
    
class ProductDetailSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    like = serializers.IntegerField(source='like_count', read_only=True)
    dislike = serializers.IntegerField(source='dislike_count', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id','category','region','title','sold',
            'price','address','phone_number','description',
            'is_active','views_count','created_at',
            'user','image_urls','like','dislike'
        ]

class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = '__all__'
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        

class ComplaintSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = [ 'id','created_at','text','product','user','is_saw'
                  ]
    
    def get_product(self,obj):
        request = self.context.get('request')
        return ProductSerializer(obj.product, context={'request': request}).data