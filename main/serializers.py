from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import *
class CustomRegisterSerializer(RegisterSerializer):
    username = None  # ✅ Usernameni butunlay olib tashlaymiz

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
          
        }
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','phone','first_name','last_name']