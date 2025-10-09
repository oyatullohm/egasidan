# services/fcm_service.py
import requests

from Admin import settings
from django.core.exceptions import ObjectDoesNotExist

class FCMService:
    @staticmethod
    def send_push_notification(fcm_token, title, body, data=None):
        url = 'https://fcm.googleapis.com/fcm/send'
        
        headers = {
            'Authorization': f'key={settings.FIREBASE_SERVER_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'to': fcm_token,
            'notification': {
                'title': title,
                'body': body,
                'sound': 'default'
            },
            'data': data or {}
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.status_code == 200
        except Exception as e:
            print(f"FCM Error: {e}")
            return False