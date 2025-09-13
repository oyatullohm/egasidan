from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True
    
    def clean_username(self, username, shallow=False):
        # Username ni tozalash jarayonini o'chirib qo'yamiz
        return ""
    
    def populate_username(self, request, user):
        # Username ni avtomatik to'ldirish jarayonini o'chirib qo'yamiz
        pass
    
    def generate_unique_username(self, txts, regex=None):
        # Noyob username generatsiya qilish jarayonini o'chirib qo'yamiz
        return ""