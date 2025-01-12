# Real-Time Encrypted Chat Application

**Project Description**

This project is a web-based chat application designed to enable secure and real-time communication between users. The application supports one-on-one and group messaging, voice and video calls, all while ensuring end-to-end encryption for enhanced privacy.

**Features**

*   **Registration and Login:**
    *   User registration with email and password.
    *   Secure login for registered users.

*   **One-on-One Messaging:**
    *   Private conversations with other users.
    *   Sending and receiving text messages, emojis, and images.
    *   Display of message read status (single/double tick).

*   **Group Rooms:**
    *   Creation of group rooms for collaborative chats.
    *   Naming rooms and inviting users.
    *   Option to set passwords for rooms.

*    **Group Messaging:**
      *   Messaging in groups, sharing emojis and images.
       *   Display of message read status (single/double tick).

*   **Real-Time Communication:**
    *   Instant message exchange using WebSocket technology.

*   **Security:**
    *   End-to-end encryption to ensure message privacy (symmetric encryption).

*   **Voice and Video Calling:**
    *   Real-time voice and video calls in group rooms using WebRTC.

**Technologies**

*   **Backend:**
    *   Python (Django Framework)
    *   Django Channels (WebSocket)
*   **Frontend:**
    *   HTML, CSS, JavaScript (vanilla JS)
*   **Database:**
    *   Firebase Firestore
*   **Image Upload:**
    *   Cloudinary API
*   **Voice/Video Calling:**
     * WebRTC

**Setup**

1.  **Clone the Repository:**
    ```
    git clone https://github.com/ba2hannn/realtime-encrypted-chat.git
    ```

2.  **Install Backend Dependencies:**
    ```
    pip install -r requirements.txt
    ```

3.  **Configure Firebase Firestore and Cloudinary Settings:**
    *   Update the Firebase API key and Cloudinary `cloud_name`, `api_key`, and `api_secret` values in the `RealTimeChat/settings.py` file. (Important: It is recommended to manage sensitive data with environment variables).
     * Download and include the service account json file into the project from the Firebase console.
4.  **Run the Backend Server:**
    ```
    python manage.py migrate
    python manage.py runserver
    ```

**Usage**

1.  Log in or sign up for the application.
2.  Start a one-on-one or group chat.
3.  Write messages, send emojis or images.
4.  Initiate a voice or video call.

**Additional Notes**

*   Placeholder values are used instead of the real API keys and credentials. Please update these variables accordingly. Using environment variables is highly recommended.
*   This project is continuously under development.
*   Contributions and feedback are appreciated.

**Contributing**

*   If you would like to contribute to this project, please submit a pull request with a branch of your own.
*   For bug reports and feature requests, please use GitHub Issues.
