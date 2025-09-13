from django.utils.text import slugify
from rest_framework.response import Response
def unique_slug(instance, new_slug=None):
    """
    Foydalanuvchi bo'yicha unique slug yaratadi.
    Agar slug allaqachon mavjud bo'lsa, -1, -2 ... qo'shadi.
    """
    slug = new_slug or slugify(instance.name)
    Klass = instance.__class__
    
    # Faqat shu foydalanuvchining yozuvlarini tekshiradi
    qs = Klass.objects.filter(user=instance.user, slug=slug)
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)
    
    if qs.exists():
        i = 1
        new_slug = f"{slug}-{i}"
        while Klass.objects.filter(user=instance.user, slug=new_slug).exists():
            i += 1
            new_slug = f"{slug}-{i}"
        slug = new_slug
    return slug
