# allauth utils.py faylini patch qilish
from allauth import utils
from django.core.exceptions import FieldDoesNotExist

original_get_username_max_length = utils.get_username_max_length

def patched_get_username_max_length():
    try:
        return original_get_username_max_length()
    except FieldDoesNotExist:
        # Agar username maydoni topilmasa, 0 qaytaramiz
        return 0

utils.get_username_max_length = patched_get_username_max_length