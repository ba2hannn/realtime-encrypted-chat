<div align="center">

# Real-Time Encrypted Chat

### End-to-End Encrypted Messaging with Voice & Video

*A secure, real-time chat application with one-on-one messaging, group rooms, and WebRTC voice/video calling. All messages are end-to-end encrypted for privacy.*

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white)
![WebRTC](https://img.shields.io/badge/WebRTC-333333?style=flat-square&logo=webrtc&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=flat-square&logo=firebase&logoColor=black)
![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=flat-square&logo=websocket&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

[Features](#-features) • [Tech Stack](#-tech-stack) • [Getting Started](#-getting-started) • [Usage](#-usage)

</div>

---

## About

A web-based chat platform designed for **secure and private communication**. Built with Django Channels for real-time WebSocket messaging and WebRTC for peer-to-peer voice/video calls. All messages are end-to-end encrypted to ensure privacy.

## Features

| Feature | Description |
|---------|-------------|
| **User Authentication** | Secure registration and login system |
| **One-on-One Messaging** | Private conversations with any user |
| **Group Chat Rooms** | Public or password-protected rooms |
| **End-to-End Encryption** | Messages encrypted before transmission |
| **Voice & Video Calls** | Real-time WebRTC calls within group rooms |
| **Image Sharing** | Share images via Cloudinary integration |
| **Read Receipts** | Track message delivery status |
| **Real-Time Delivery** | Instant message delivery via WebSockets |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Django, Django Channels, Daphne (ASGI) |
| **Frontend** | HTML, CSS, Vanilla JavaScript |
| **Real-Time** | WebSockets, WebRTC |
| **Database** | Firebase Firestore & Realtime Database (chat), SQLite (auth) |
| **Storage** | Cloudinary (image uploads) |

## Architecture

```
┌──────────────────────────────────────────────┐
│              Browser Client                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  Chat UI  │  │  WebRTC  │  │  E2E Enc  │  │
│  └─────┬────┘  └─────┬────┘  └───────────┘  │
└────────┼─────────────┼───────────────────────┘
         │ WebSocket    │ WebRTC (P2P)
┌────────▼─────────────▼───────────────────────┐
│           Django + Channels                   │
│  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Daphne ASGI │  │  WebSocket Consumer  │  │
│  └──────┬───────┘  └──────────┬───────────┘  │
└─────────┼─────────────────────┼──────────────┘
          │                     │
┌─────────▼──────┐  ┌──────────▼───────────────┐
│ Firebase        │  │  Cloudinary              │
│ (Messages +     │  │  (Image Storage)         │
│  Realtime DB)   │  │                          │
└─────────────────┘  └──────────────────────────┘
```

## Project Structure

```
RealTimeChat/
├── ChatApp/                # Core Django app
│   ├── consumers.py        # WebSocket consumer for real-time events
│   ├── models.py           # Django models
│   ├── views.py            # Views for rendering pages
│   └── urls.py             # URL patterns
├── ChatProject/            # Django project settings
│   ├── settings.py         # Project configuration
│   ├── asgi.py             # ASGI entry point for Channels
│   └── urls.py             # Root URL configuration
├── templates/              # HTML templates
├── static/                 # CSS and JavaScript
├── firebase_config.py      # Firebase initialization
├── config/                 # Firebase config files
└── manage.py               # Django CLI
```

## Getting Started

### Prerequisites

- Python 3.9+
- A [Firebase](https://firebase.google.com/) project
- A [Cloudinary](https://cloudinary.com/) account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ba2hannn/realtime-encrypted-chat.git
   cd realtime-encrypted-chat
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Firebase**
   - Download service account key from Firebase Console → Project Settings → Service Accounts
   - Save as `RealTimeChat/config/firebaseAdmin_config.json`
   - Create `RealTimeChat/config/pyrebase_config.json` with your web app's Firebase config

4. **Configure Cloudinary**
   Set environment variables:
   ```bash
   export CLOUDINARY_CLOUD_NAME=your_cloud_name
   export CLOUDINARY_API_KEY=your_api_key
   export CLOUDINARY_API_SECRET=your_api_secret
   ```

5. **Run migrations and start server**
   ```bash
   python RealTimeChat/manage.py migrate
   python RealTimeChat/manage.py runserver
   ```

   Open `http://127.0.0.1:8000` in your browser.

## Usage

1. Sign up for a new account or log in
2. Create a new chat room or join an existing one
3. Start messaging, sharing images, or initiate a voice/video call

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built by [ba2hannn](https://github.com/ba2hannn)

</div>
