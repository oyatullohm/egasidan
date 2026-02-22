import firebase_admin
from firebase_admin import credentials
from Admin.settings import HOME_URL
# cred = credentials.Certificate("/var/www/egasidan/Admin/firebase/service_account.json")
cred = credentials.Certificate(HOME_URL)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)