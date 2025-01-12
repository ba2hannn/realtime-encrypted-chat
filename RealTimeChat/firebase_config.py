import firebase_admin
import pyrebase
from firebase_admin import credentials, firestore
import json

# Firebase Admin SDK için hizmet anahtarını yükleyin
cred = credentials.Certificate("config/firebaseAdmin_config.json")

# Firebase Admin SDK'yı başlatın
firebase_admin.initialize_app(cred)

# Firestore referansını alın
firestoreDB = firestore.client()

# Pyrebase için config.json dosyasını okur
with open("config/pyrebase_config.json", "r") as config_file:
    firebaseConfig = json.load(config_file)

# Pyrebase ile Firebase uygulamasını başlat
firebase=pyrebase.initialize_app(firebaseConfig)

# Firebase Authentication (kimlik doğrulama) nesnesini oluştur
authe=firebase.auth()

# Firebase Realtime Database (gerçek zamanlı veritabanı) nesnesini oluştur
realTimeDB = firebase.database()