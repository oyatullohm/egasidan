import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/var/www/egasidan/Admin/firebase/service_account.json")
# cred = credentials.Certificate("/home/dell/Desktop/Egasidan/Admin/firebase/service_account.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)