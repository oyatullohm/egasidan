from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

# TokenModel muammosini hal qilish
if hasattr(settings, 'DJ_REST_AUTH') and settings.DJ_REST_AUTH.get('TOKEN_MODEL') is None:
    try:
        from dj_rest_auth.models import TokenModel
        TokenModel = None
    except:
        pass

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError("Email yoki Phone bo'lishi kerak")
        
        user = self.model(
            email=self.normalize_email(email) if email else None,
            phone=phone,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # ✅ Login uchun email ishlatiladi
    REQUIRED_FIELDS = []  # ✅ Username talab qilinmaydi

    def __str__(self):
        return self.email if self.email else self.phone

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()