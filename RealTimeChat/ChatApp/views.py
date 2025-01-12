from django.shortcuts import render, redirect
from firebase_config import firestoreDB,realTimeDB,authe
from firebase_admin import firestore
from django.contrib import auth
import json
from django.http import JsonResponse
from google.auth.exceptions import GoogleAuthError
import bcrypt

"""
def deneme(request):
    return render(request, 'deneme.html')

def get_old_messages(request, room_name):
    # Firestore'dan mesajları sorgula
    room_ref = firestoreDB.collection('rooms').document(room_name)
    messages_ref = room_ref.collection('messages')

    # Mesajları tarih sırasına göre al (yeniye doğru)
    messages = messages_ref.order_by('timestamp').stream()

    # Mesajları formatla
    old_messages = []
    for message in messages:
        old_messages.append({
            'sender': message.get('sender'),
            'message': message.get('message')
        })

    # Eski mesajları JSON olarak döndür
    return JsonResponse({'old_messages': old_messages})
"""

"""
def CreateRoom(request):
    if 'uid' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        room = request.POST['room']
        session_id = request.session['uid']
        user_info = authe.get_account_info(session_id) 
        user_id = user_info['users'][0]['localId']

        try:
            Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=user_id)

        except Room.DoesNotExist:
            new_room = Room(room_name = room)
            new_room.save()
            return redirect('room', room_name=room, username=user_id)

    return render(request, 'create_room.html')
"""

"""
def MessageView(request, room_name, username):
    if 'uid' not in request.session:
        return redirect('login')
    
    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']

        print(message)

        new_message = Message(room=get_room, sender=username,senderName=request.session['username'], message=message)
        new_message.save()

    get_messages= Message.objects.filter(room=get_room)
    
    context = {
        "messages": get_messages,
        "username": username,
        "room_name": room_name,
        "sendername":request.session['username'],
    }
    return render(request, 'message.html', context)

def PrivateMessageView(request, receiverName ,senderName ):
    if 'uid' not in request.session:
        return redirect('login')
    
    context = {
        "username": senderName,
        "receiverName":receiverName,
    }

    return render(request, 'private_chat.html', context)
"""

#Hesap İşlemleri

#Login

def Login(request):
    auth.logout(request)
    
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get("password")
            user = authe.sign_in_with_email_and_password(email, password)

            # Kullanıcı bilgilerini al
            user_info = authe.get_account_info(user['idToken'])
            is_verified = user_info['users'][0].get('emailVerified', False)  # Doğrulama durumu

            # Doğrulama kontrolü
            if not is_verified:
                error = "Your email is not verified. Please check your inbox and verify your email."
                return render(request, "login.html", {"error": error})

            # Giriş başarılı, oturum bilgilerini kaydet
            sessionId = user['idToken']
            user_id = user_info['users'][0]['localId']
            user_ref = firestoreDB.collection('users').document(user_id).get()

            if user_ref.exists:
                username = user_ref.to_dict().get('username', 'AnonymousUser')
            else:
                username = "AnonymousUser"

            request.session['uid'] = str(user_id)
            request.session['username'] = str(username)
            return redirect('chat-list')

        except:
            error = "Invalid email or password."
            return render(request, "login.html", {"error": error})

    return render(request, "login.html")

#Signup
def Signup(request):
    auth.logout(request)

    if request.method == "POST":
        try:
            email = request.POST.get('email')
            password = request.POST.get("password")
            againPassword = request.POST.get("againPassword")

            if password != againPassword:
                error = "Passwords do not match."
                return render(request, "signup.html", {"error": error})

            username = request.POST.get('username')
            user = authe.create_user_with_email_and_password(email, password)
            user_id = user['localId']

            # Kullanıcıyı Firestore'a ekle
            user_ref = firestoreDB.collection('users').document(user_id)
            user_ref.set({
                "username": username,
            })

            # E-posta doğrulama bağlantısı gönder
            authe.send_email_verification(user['idToken'])

        except:
            error = "Invalid credentials."
            return render(request, "signup.html", {"error": error})

        # Kullanıcıya bir doğrulama mesajı göster
        return redirect('login')

    return render(request, "signup.html")
    
#logout
def Logout(request):
    auth.logout(request)
    return redirect('login')

# Forgot Password
def ForgotPassword(request):
    auth.logout(request)

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            authe.send_password_reset_email(email)
            success = "Password reset email has been sent. Please check your inbox."
            return render(request, "forgot_password.html", {"success": success})
        except:
            error = "An error occurred. Please check the email address and try again."
            return render(request, "forgot_password.html", {"error": error})

    return render(request, "forgot_password.html")

# Voice Room
def VoiceRoom(request, voice_chat):
    if 'uid' not in request.session:
        return redirect('login')
    
    room_doc = firestoreDB.collection('rooms').document(voice_chat).get()

    room_data = room_doc.to_dict()

    return render(request, 'sesli_mesajlaşma.html', {
        'room_name': room_data['room_name'],
        'voice_chat': voice_chat,
        "userID": request.session['uid'],
        "userName" : request.session['username'],
    })

# Chat list and chat 
def ChatList(request):
    if 'uid' not in request.session:
        return redirect('login')
    
    context = {
        "userID": request.session['uid'],
    }
    
    return render(request,"chat_list.html", context)

# Room list and room chat
def RoomList(request):
    if 'uid' not in request.session:
        return redirect('login')
    
    context = {
        "userID": request.session['uid'],
        "userName" : request.session['username'],
    }
    
    return render(request,"room_list.html", context)

# Create Room
def RoomCreate(request):
    if 'uid' not in request.session:
        return redirect('login')
   
    if request.method == "POST":
        try:
            room_name = request.POST.get('room-name')
            room_password = request.POST.get('room-password') # get the password 
            
            if not room_name:
                return render(request, "room_create.html", {"error": "Room name cannot be empty."})
           
            # Create new room document
            room_doc = firestoreDB.collection('rooms').document()
            
            # Hash the password if one is provided
            hashed_password = None
            if room_password:
                # Example of secure hashing logic
                hashed_password = bcrypt.hashpw(room_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                

            # Add info subcollection
            room_doc.set({
                'room_name': room_name,
                'CreationDate': firestore.SERVER_TIMESTAMP,
                'room_password': hashed_password if room_password else None
            })
            
            return redirect('room-list')
            
        except Exception as e:
            return render(request, "room_create.html", {"error": f"An error occurred: {str(e)}"})
            
    return render(request, "room_create.html")

def verify_room_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_name = data.get('room_name')
            password = data.get('password')

            if not room_name or not password:
                return JsonResponse({'success': False, 'error': 'Room name or password missing.'})

            room_doc = firestoreDB.collection('rooms').document(room_name).get()
            if not room_doc.exists:
                 return JsonResponse({'success': False, 'error': 'Room not found.'})
                 
            room_data = room_doc.to_dict()
            hashed_password = room_data.get('room_password')

            if hashed_password is None:
                 return JsonResponse({'success': True}) # Eğer şifre yoksa her zaman true döndür.

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return JsonResponse({'success': True})
            else:
                 return JsonResponse({'success': False, 'error': 'Incorrect password.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})