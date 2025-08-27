# Real-Time Encrypted Chat Application

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A web-based, real-time chat application designed for secure and private communication. It supports one-on-one messaging, group chats, and real-time voice/video calls with end-to-end encryption.

## ✨ Features

-   **👤 User Authentication:** Secure user registration and login system.
-   **💬 One-on-One Messaging:** Engage in private conversations with other users.
-   **👨‍👩‍👧‍👦 Group Chat Rooms:** Create public or private (password-protected) chat rooms.
-   **🚀 Real-Time Communication:** Instant message delivery powered by Django Channels (WebSockets).
-   **🔒 End-to-End Encryption:** Messages are encrypted to ensure privacy and security.
-   **🎤 Voice & Video Calls:** High-quality, real-time voice and video communication within group rooms using WebRTC.
-   **🖼️ Media Sharing:** Share images within chats, hosted via Cloudinary.
-   **✅ Read Receipts:** See the status of your messages (sent/delivered).

## 🛠️ Technologies Used

| Category      | Technology                                                                                             |
| :------------ | :----------------------------------------------------------------------------------------------------- |
| **Backend**   | [Python](https://www.python.org/), [Django](https://www.djangoproject.com/), [Django Channels](https://channels.readthedocs.io/en/stable/), [Daphne](https://github.com/django/daphne) |
| **Frontend**  | HTML, CSS, Vanilla JavaScript                                                                          |
| **Real-Time** | [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API), [WebRTC](https://webrtc.org/) |
| **Database**  | [Firebase Firestore](https://firebase.google.com/docs/firestore) & [Realtime Database](https://firebase.google.com/docs/database) (for chat), SQLite (for Django admin) |
| **Storage**   | [Cloudinary](https://cloudinary.com/) (for image uploads)                                              |
| **Deployment**| (Not specified, but compatible with services supporting ASGI)                                          |

## 📂 Project Structure

```
├── RealTimeChat/
│   ├── ChatApp/            # Core Django app for chat logic
│   │   ├── consumers.py    # WebSocket consumer for real-time events
│   │   ├── models.py       # Django models (if any, most data is on Firebase)
│   │   ├── views.py        # Views for rendering pages
│   │   └── urls.py         # URL patterns for the ChatApp
│   ├── ChatProject/        # Main Django project settings
│   │   ├── settings.py     # Project settings
│   │   ├── asgi.py         # ASGI entry point for Channels
│   │   └── urls.py         # Root URL configuration
│   ├── templates/          # HTML templates
│   ├── static/             # CSS and JavaScript files
│   ├── firebase_config.py  # Firebase initialization logic
│   ├── config/             # Folder for Firebase config files
│   └── manage.py           # Django's command-line utility
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.9+
-   `pip` and `virtualenv`
-   A [Firebase](https://firebase.google.com/) project
-   A [Cloudinary](https://cloudinary.com/) account

### ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ba2hannn/realtime-encrypted-chat.git
    cd realtime-encrypted-chat
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Firebase:**
    a. Go to your Firebase project console.
    b. **Service Account (Admin SDK):**
       - Navigate to `Project Settings > Service accounts`.
       - Click "Generate new private key" and download the JSON file.
       - Rename this file to `firebaseAdmin_config.json` and place it inside the `RealTimeChat/config/` directory.
    c. **Web App SDK (Pyrebase):**
       - In your Firebase project, go to `Project Settings > General`.
       - Scroll down to "Your apps" and click the `</>` icon to create a new web app (or use an existing one).
       - You will be given a `firebaseConfig` object. Copy this JSON object.
       - Create a new file named `pyrebase_config.json` inside `RealTimeChat/config/` and paste the `firebaseConfig` object into it.

5.  **Configure Cloudinary:**
    - The application expects Cloudinary credentials to be available. The recommended way is to use environment variables. The code in `views.py` will look for:
        - `CLOUDINARY_CLOUD_NAME`
        - `CLOUDINARY_API_KEY`
        - `CLOUDINARY_API_SECRET`
    - For local development, you can hardcode these in `RealTimeChat/ChatApp/views.py`, but this is **not recommended for production**.

6.  **Apply Django Migrations:**
    (This will set up the local SQLite database used by Django for users and admin staff).
    ```bash
    python RealTimeChat/manage.py migrate
    ```

7.  **Run the development server:**
    ```bash
    python RealTimeChat/manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

## Usage

1.  Open your web browser and navigate to `http://127.0.0.1:8000`.
2.  Sign up for a new account or log in with an existing one.
3.  Create a new chat room or join an existing one.
4.  Start sending messages, sharing images, or initiate a voice/video call.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or have found a bug, please follow these steps:

1.  **Fork the Project:** Click the 'Fork' button at the top right of this page.
2.  **Create a New Branch:**
    ```bash
    git checkout -b feature/YourAmazingFeature
    ```
3.  **Commit Your Changes:**
    ```bash
    git commit -m 'Add some AmazingFeature'
    ```
4.  **Push to the Branch:**
    ```bash
    git push origin feature/YourAmazingFeature
    ```
5.  **Open a Pull Request:** Go back to the original repository and click 'New pull request'.

Please make sure to write clear commit messages and provide a detailed description for your pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
