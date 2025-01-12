import json
from channels.generic.websocket import AsyncWebsocketConsumer
from firebase_config import firestoreDB  
from firebase_admin import firestore_async, firestore
import cloudinary
import cloudinary.uploader
import base64
import io

# Genel Sohbet Tüketicisi
class ChatConsumer(AsyncWebsocketConsumer):
    # WebSocket bağlantısı kurulduğunda çalışır
    async def connect(self):
        # Oda adını URL'den al ve formatla
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        # Kanal katmanına odayı ekle
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        # Bağlantıyı kabul et
        await self.accept()

    # WebSocket bağlantısı koptuğunda çalışır
    async def disconnect(self, close_code):
        # Kanal katmanından odayı çıkar
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # WebSocket'ten mesaj alındığında çalışır
    async def receive(self, text_data):
        # Mesajı JSON formatından Python objesine çevir
        text_data_json = json.loads(text_data)

        # Mesajı kanal katmanına gönder
        event = {
                'type': 'send_message',
                'message': text_data_json,
            }
        
        await self.channel_layer.group_send(self.room_name, event)

    # Kanal katmanından mesaj alındığında çalışır
    async def send_message(self, event):
        # Mesajı al
        data = event['message']
        # Mesaj türünü al
        message_type = data['type']

        # Mesaj türüne göre işlem yap
        if message_type == 'message':
            # Mesajı oluştur ve Firestore'a kaydet
            await self.create_message(data=data)
            # Yanıt verisini oluştur
            response_data = {
                'type' : data['type'],
                'sender': data['sender'],
                'message': data['message'],
                'sendername': data['sendername'],
                'messageID': data['messageID'],
            }
            # Mesajı WebSocket üzerinden gönder
            await self.send(text_data=json.dumps({'message': response_data}))
            
        elif message_type == 'read_status':
            # Mesajın okundu durumunu güncelle
            await self.update_message_status(data=data)
            # Yanıt verisini oluştur
            response_data = {
                'type' : data['type'],
                'messageID': data['messageID'],
            }
            # Mesajı WebSocket üzerinden gönder
            await self.send(text_data=json.dumps({'message': response_data}))

        elif message_type == 'image':
            # Resmi yükle ve URL'sini al
            image_url = await self.handle_image(data=data)
            # Yanıt verisini oluştur
            response_data = {
                'type': data['type'],
                'sender': data['sender'],
                'message': image_url,
                'sendername': data['sendername'],
                'messageID': data['messageID'],
            }
            # Mesajı WebSocket üzerinden gönder
            await self.send(text_data=json.dumps({'message': response_data}))
           
    # Firestore'a mesaj kaydetme fonksiyonu
    async def create_message(self, data):
        # Mesaj verilerini al
        room_name = data['room_name']
        sender = data['sender']
        message = data['message']
        senderName = data['sendername']
        messageId = data['messageID']

        # Firestore'dan oda referansını al
        room_ref = firestoreDB.collection('rooms').document(room_name)
        # Mesajlar koleksiyonundan mesaj referansını al
        messages_ref = room_ref.collection('messages').document(messageId)

        # Aynı mesaj zaten var mı kontrol et
        existing_message = messages_ref.get()

        if existing_message.exists:
            return

        # Mesajı Firestore'a kaydet
        messages_ref.set({
            'sender': sender,
            'message': message,
            'senderName': senderName,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'isRead': False,
            'type' : 'message'
        })

    # Firestore'da mesajın okundu durumunu güncelleme fonksiyonu
    async def update_message_status(self, data):
        # Mesaj verilerini al
        room_name = data['room_name']
        messageId = data['messageID']

        # Firestore'dan oda referansını al
        room_ref = firestoreDB.collection('rooms').document(room_name)
        # Mesajlar koleksiyonundan mesaj referansını al
        messages_ref = room_ref.collection('messages').document(messageId)

        # Mesaj var mı kontrol et
        message_doc = messages_ref.get()
        if message_doc.exists:
            # Mesajın okundu durumunu güncelle
            messages_ref.update({
                'isRead': True
            })
        else:
            # Mesaj yoksa konsola yazdır
            print(f"Message document with ID {messageId} does not exist in chat {room_name}.")

    # Resmi yükleme ve Firestore'a kaydetme fonksiyonu
    async def handle_image(self,data):
        # Cloudinary ayarlarını yapılandır
        cloudinary.config(
            cloud_name = "example_cloud_name",
            api_key = "example_api_key",
            api_secret = "example_api_secret",
            secure = True
        )

        # Mesaj verilerini al
        image_data = data['message']
        sender = data['sender']
        senderName = data['sendername']
        messageId = data['messageID']
        room_name = data['room_name']

        # Base64 ile kodlanmış resmi çöz
        image_bytes = io.BytesIO()
        image_bytes.write(base64.b64decode(image_data.split(',')[1]))
        image_bytes.seek(0)

        # Resmi Cloudinary'ye yükle
        result = cloudinary.uploader.upload(
            image_bytes,
            folder="chat_images" 
        )
        # Firestore'dan oda referansını al
        room_ref = firestoreDB.collection('rooms').document(room_name)
        # Mesajlar koleksiyonundan mesaj referansını al
        messages_ref = room_ref.collection('messages').document(messageId)

        # Mesajı Firestore'a kaydet
        messages_ref.set({
            'sender': sender,
            'senderName': senderName,
            'message': result['secure_url'],
            'timestamp': firestore.SERVER_TIMESTAMP,
            'isRead': False,
            'type' : 'image'
        })
        # Resmin URL'sini döndür
        return result['secure_url']

# Özel Sohbet Tüketicisi
class PrivateChatConsumer(AsyncWebsocketConsumer):
     # WebSocket bağlantısı kurulduğunda çalışır
    async def connect(self):
        # Sohbet adını URL'den al ve formatla
        self.chat_name = f"chat_{self.scope['url_route']['kwargs']['chat_name']}"
        # Kanal katmanına sohbeti ekle
        await self.channel_layer.group_add(self.chat_name, self.channel_name)
        # Bağlantıyı kabul et
        await self.accept()

    # WebSocket bağlantısı koptuğunda çalışır
    async def disconnect(self, close_code):
        # Kanal katmanından sohbeti çıkar
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)

    # WebSocket'ten mesaj alındığında çalışır
    async def receive(self, text_data):
         # Mesajı JSON formatından Python objesine çevir
        text_data_json = json.loads(text_data)
        message = text_data_json

         # Mesajı kanal katmanına gönder
        event = {
            'type': 'send_message',
            'message': message,
        }
        
        await self.channel_layer.group_send(self.chat_name, event)
    
    # Kanal katmanından mesaj alındığında çalışır
    async def send_message(self, event):
         # Mesajı al
        data = event['message']
        # Mesaj türünü al
        message_type = data['type']

        # Mesaj türüne göre işlem yap
        if message_type == 'message':
            # Mesajı oluştur ve Firestore'a kaydet
            await self.create_message(data=data)
            # Yanıt verisini oluştur
            response_data = {
                'type': data['type'],
                'sender': data['sender'],
                'message': data['message'],
                'receiver': data['receiver'],
                'messageID': data['messageID']
            }
            # Mesajı WebSocket üzerinden gönder
            await self.send(text_data=json.dumps({'message': response_data}))
            
        elif message_type == 'read_status':
            # Mesajın okundu durumunu güncelle
            await self.update_message_status(data=data)
            # Yanıt verisini oluştur
            response_data = {
                'type': data['type'],
                'messageID': data['messageID']
            }
             # Mesajı WebSocket üzerinden gönder
            await self.send(text_data=json.dumps({'message': response_data}))

        elif message_type == 'image':
            # Resmi yükle ve URL'sini al
            image_url = await self.handle_image(data=data)
             # Yanıt verisini oluştur
            response_data = {
                'type': data['type'],
                'sender': data['sender'],
                'message': image_url,
                'receiver': data['receiver'],
                'messageID': data['messageID'],
            }
            # Mesajı WebSocket üzerinden gönder
            await self.send(text_data=json.dumps({'message': response_data}))

    # Firestore'a mesaj kaydetme fonksiyonu
    async def create_message(self, data):
        # Mesaj verilerini al
        sender = data['sender']
        message = data['message']
        receiver = data['receiver']
        messageId = data['messageID']

        # Kullanıcıları sırala ve sohbet ID'sini oluştur
        sorted_users = sorted([sender, receiver])
        chat_id = f"{sorted_users[0]}_{sorted_users[1]}"

        # Firestore'dan özel sohbet referansını al
        private_chats_ref = firestoreDB.collection('private_chats').document(chat_id)
        # Mesajlar koleksiyonundan mesaj referansını al
        messages_ref = private_chats_ref.collection('messages').document(messageId)

        # Aynı mesaj zaten var mı kontrol et
        existing_message = messages_ref.get()

        if existing_message.exists:
            return  

        # Mesajı Firestore'a kaydet
        messages_ref.set({
            'sender': sender,
            'receiver': receiver,
            'message': message,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'isRead': False,
            'type' : 'message'
        })

    # Firestore'da mesajın okundu durumunu güncelleme fonksiyonu
    async def update_message_status(self, data):
        # Mesaj verilerini al
        sender = data['sender']
        receiver = data['receiver']
        messageId = data['messageID']

        # Kullanıcıları sırala ve sohbet ID'sini oluştur
        sorted_users = sorted([sender, receiver])
        chat_id = f"{sorted_users[0]}_{sorted_users[1]}"

        # Firestore'dan özel sohbet referansını al
        private_chats_ref = firestoreDB.collection('private_chats').document(chat_id)
         # Mesajlar koleksiyonundan mesaj referansını al
        messages_ref = private_chats_ref.collection('messages').document(messageId)

        # Mesaj var mı kontrol et
        message_doc = messages_ref.get()
        if message_doc.exists:
             # Mesajın okundu durumunu güncelle
            messages_ref.update({
                'isRead': True
            })
        else:
            # Mesaj yoksa konsola yazdır
            print(f"Message document with ID {messageId} does not exist in chat {chat_id}.")

    # Resmi yükleme ve Firestore'a kaydetme fonksiyonu
    async def handle_image(self,data):
        # Cloudinary ayarlarını yapılandır
        cloudinary.config( 
            cloud_name = "dujinwed7",
            api_key = "698466817525883", 
            api_secret = "b0kwP94CLb8TEPP-ni0IBSQ0ly8",
            secure=True
        )

        # Mesaj verilerini al
        image_data = data['message']
        sender = data['sender']
        receiver = data['receiver']
        messageId = data['messageID']

        # Base64 ile kodlanmış resmi çöz
        image_bytes = io.BytesIO()
        image_bytes.write(base64.b64decode(image_data.split(',')[1]))
        image_bytes.seek(0)

        # Resmi Cloudinary'ye yükle
        result = cloudinary.uploader.upload(
            image_bytes,
            folder="chat_images" 
        )
        # Kullanıcıları sırala ve sohbet ID'sini oluştur
        sorted_users = sorted([sender, receiver])
        chat_id = f"{sorted_users[0]}_{sorted_users[1]}"

        # Firestore'dan özel sohbet referansını al
        private_chats_ref = firestoreDB.collection('private_chats').document(chat_id)
        # Mesajlar koleksiyonundan mesaj referansını al
        messages_ref = private_chats_ref.collection('messages').document(messageId)

         # Mesajı Firestore'a kaydet
        messages_ref.set({
            'sender': sender,
            'receiver': receiver,
            'message': result['secure_url'],
            'timestamp': firestore.SERVER_TIMESTAMP,
            'isRead': False,
            'type' : 'image'
        })
        # Resmin URL'sini döndür
        return result['secure_url']

# Sesli Sohbet Tüketicisi
class VoiceChatConsumer(AsyncWebsocketConsumer):
    connected_users = {}  
   
    # WebSocket bağlantısı kurulduğunda çalışır
    async def connect(self):
        # Oda adını URL'den al
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # Oda grup adını oluştur
        self.room_group_name = f'voice_chat_{self.room_name}'
         # Query parametrelerini al
        query_string = self.scope.get('query_string', b'').decode()
        query_params = dict(param.split('=') for param in query_string.split('&') if param)
         # Kullanıcı ID'sini ve adını al
        self.user_id = query_params.get('userId', '')
        self.user_name = query_params.get('userName', '')
       
        # Oda için katılımcı listesi yoksa oluştur
        if self.room_group_name not in self.connected_users:
            self.connected_users[self.room_group_name] = {}
           
        # Kullanıcı verilerini oluştur
        user_data = {
            'peer_id': self.channel_name,
            'user_name': self.user_name,
            'userID': self.user_id
        }
       
        # Kullanıcıyı katılımcı listesine ekle
        self.connected_users[self.room_group_name][self.channel_name] = user_data
       
        # Kanal katmanına odayı ekle
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # Bağlantıyı kabul et
        await self.accept()
       
        # Yeni kullanıcıyı gruba yayınla
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'peer_message',
                'message': {
                    'type': 'new_peer',
                    **user_data
                }
            }
        )

    # WebSocket bağlantısı koptuğunda çalışır
    async def disconnect(self, close_code):
        # Oda için katılımcı listesi varsa
        if self.room_group_name in self.connected_users:
             # Kullanıcı katılımcı listesindeyse sil
            if self.channel_name in self.connected_users[self.room_group_name]:
                del self.connected_users[self.room_group_name][self.channel_name]
            
            # Eğer odada hiç katılımcı kalmadıysa, oda listesinden sil
            if not self.connected_users[self.room_group_name]:
                del self.connected_users[self.room_group_name]
        
        # Kullanıcının ayrıldığını gruba yayınla
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'peer_message',
                'message': {
                    'type': 'peer_disconnected',
                    'peer_id': self.channel_name,
                    'user_name': self.user_name,
                    'userID': self.user_id
                }
            }
        )
        # Kanal katmanından odayı çıkar
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # WebSocket'ten mesaj alındığında çalışır
    async def receive(self, text_data):
         # Mesajı JSON formatından Python objesine çevir
        data = json.loads(text_data)
       
        # Katılımcıları isteme mesajıysa
        if data.get('type') == 'get_participants':
            # Eğer oda için katılımcı listesi varsa
            if self.room_group_name in self.connected_users:
                # Katılımcı verilerini al
                participants_data = list(self.connected_users[self.room_group_name].values())
                # Katılımcıları WebSocket üzerinden gönder
                await self.send(json.dumps({
                    'type': 'current_participants',
                    'participants': participants_data
                }))
            return
        # Hedef varsa, mesajı ilgili kullanıcıya gönder
        if 'target' in data:
            # Mesaj verilerini oluştur
            message_data = {
                **data,
                'peer_id': self.channel_name,
                'user_name': self.user_name,
                'userID': self.user_id
            }
            # Mesajı kanal katmanına gönder
            await self.channel_layer.send(
                data['target'],
                {
                    'type': 'peer_message',
                    'message': message_data
                }
            )
    # Kanal katmanından mesaj alındığında çalışır
    async def peer_message(self, event):
        # Mesajı WebSocket üzerinden gönder
        await self.send(text_data=json.dumps(event['message']))