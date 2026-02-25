from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    LEVEL_CHOICES = (
        (1, 'Category'),
        (2, 'SubCategory'),
        (3, 'SubSubCategory'),
    )
    img = models.ImageField(upload_to='categories/',null=True,blank=True)
    name = models.CharField(max_length=100)
    
    category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
    )
    level = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICES,
        editable=False,
        db_index=True
    )

    def save(self, *args, **kwargs):
        if self.category is None:
            self.level = 1
        else:
            self.level = self.category.level + 1
        super().save(*args, **kwargs)
    def __str__(self):
        return "{} - {}".format(self.name, self.level)

class Model(models.Model):
    """ bu mahsulot modeli uchun model """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='models')

    def __str__(self):
        return self.name


class Region(models.Model):
    """ bu mahsulot joylashgan hududlar uchun model """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    """ bu mahsulot rasmlari uchun model """
    image = models.ImageField(upload_to='product_images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded at {self.uploaded_at}"


class Product(models.Model):

    SOLD_CHOICES = [
        ('sold', 'Sotilgan'),
        ('not_sold', 'Sotilmagan'),

    ]
    MONEY_CHOICES = [
        ('UZS', 'UZS'),
        ('USD', 'USD'),
    ]
    
    title = models.CharField(max_length=255) # sarlavhasi
    region = models.ForeignKey(Region, on_delete=models.CASCADE) # hududi
    sold = models.CharField(max_length=55, choices=SOLD_CHOICES, default='not_sold') # sotilgan yoki sotilmaganligi
    category = models.ForeignKey(Category, on_delete=models.CASCADE,db_index=True) # kategoriyasi
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True) # modeli masalam kia
    image = models.ManyToManyField('Image',blank=True)# rasmlari
    price = models.DecimalField(max_digits=14,decimal_places=0) # narxi
    money_type = models.CharField(max_length=10, choices=MONEY_CHOICES, default='UZS')# valyutasi UZS  USD
    trade  = models.BooleanField(default=False)# arzonlashtirish mumkinligi
    exchange = models.BooleanField(default=False)# almashish mumkinligi
    dostafca = models.BooleanField(default=False)# dostafka borligi
    address = models.TextField(blank=True)# manzili
    phone_number = models.CharField(max_length=13)# telefon raqami
    description = models.TextField(blank=True, null=True)# mahsulot haqida qo'shimcha ma'lumot
    contact_name = models.CharField(max_length=255, default='contact_name')
    condition = models.CharField(max_length=255, default='condition')
    is_active = models.BooleanField(default=True)# faol yoki nofaol    
    is_status = models.BooleanField(default=False)# vip e'lon
    views_count = models.PositiveIntegerField(default=0)# ko'rishlar soni
    created_at = models.DateTimeField(auto_now_add=True)# yaratildi
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')# foydalanuvchi
    
    lan = models.CharField(max_length=50, blank=True, null=True)# kenglik
    lat = models.CharField(max_length=50, blank=True, null=True)# uzunlik

    @property
    def image_urls(self):
        return [img.image.url for img in self.image.all()]
    def __str__(self):
        return self.title


class PriceWatch(models.Model):
    """ bu mahsulot narxini kuzatish uchun model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='price_watches')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_watches')
    last_price = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} watches {self.product.id} at {self.last_price}"


class Like(models.Model):
    """ bu mahsulot yoqtirishlar uchun model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} likes {self.product.id}"

   
class Dislike(models.Model):
    """ bu mahsulot yoqtirmasliklar uchun model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} dislikes {self.product.id}"


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaint')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True, blank=True, related_name='comentary_product')
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_saw = models.BooleanField(default=False)
    type = models.CharField(max_length=255) 


    def __str__(self):
        return f"{self.user}"

class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recent_views')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'product')
