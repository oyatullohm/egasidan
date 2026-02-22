# DevSMS API - Python Example
import requests
from Admin.settings import SMS_TOKEN

TOKEN = SMS_TOKEN
BASE_URL = "https://devsms.uz/api"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# SMS Yuborish
def send_sms(phone: str, message: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/send_sms.php",
        headers=headers,
        json={
            "phone": phone,
            "message": message
        }
    )
    return response.json()

# Balansni olish
def get_balance() -> dict:
    response = requests.get(
        f"{BASE_URL}/get_balance.php",
        headers=headers
    )
    return response.json()

# SMS tarixini olish
def get_history(limit: int = 50, offset: int = 0) -> dict:
    response = requests.get(
        f"{BASE_URL}/get_history.php",
        headers=headers,
        params={"limit": limit, "offset": offset}
    )
    return response.json()

# Ishlatish
if __name__ == "__main__":
    # SMS yuborish
    result = send_sms("998900601044", "Salom!")
    print(result)
    
    # Balansni tekshirish
    balance = get_balance()
    print(f"Balans: {balance['data']['balance']} so'm")