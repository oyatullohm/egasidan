from django.core.cache import cache
import random

VERIFY_TTL = 240  # 2 minut

def set_verify_code(code, phone):
    cache.set(
        f"verify:{code}",
        {"phone": phone},
        timeout=VERIFY_TTL
    )

def get_verify_email_by_code(code):
    # print(cache.get(f"verify:{code}"))
    return cache.get(f"verify:{code}")

def delete_verify_code(code):
    cache.delete(f"verify:{code}")