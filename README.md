# 💬 Chatterbox

A real-time chat application built with **FastAPI**, **WebSockets**, and **SQLite**. Users can register, log in, and chat with each other instantly in a shared chat room.

---

## 🚀 Features

- User registration and login with hashed passwords (bcrypt)
- Real-time messaging via WebSockets
- Persistent chat history stored in SQLite
- Animated, gradient-themed UI
- Broadcast messages to all connected users

---

## 🛠️ Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Backend   | Python, FastAPI, Uvicorn |
| Database  | SQLite (WAL mode)       |
| Auth      | bcrypt via passlib      |
| Frontend  | HTML, CSS, Vanilla JS   |
| Realtime  | WebSockets              |

---

## 📁 Project Structure

```
chatterbox/
├── app.py           # Main FastAPI application (routes, WebSocket, auth)
├── db.py            # Database connection helper
├── database.py      # Database schema setup script
├── templates/
│   └── index.html   # Frontend HTML
└── static/
    ├── script.js    # Frontend JavaScript (auth, WebSocket, UI)
    └── style.css    # Styles
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/chatterbox.git
cd chatterbox
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn passlib[bcrypt] python-multipart
```

### 4. Initialize the database

```bash
python database.py
```

### 5. Run the server

```bash
uvicorn app:app --reload
```

### 6. Open in your browser

```
http://localhost:8000
```

---

## 📡 API Endpoints

| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| GET    | `/`                | Serves the frontend UI   |
| POST   | `/register`        | Register a new user      |
| POST   | `/login`           | Login and get a token    |
| WS     | `/ws/{username}`   | WebSocket chat connection |

---

## 🔐 Authentication

- Passwords are hashed using **bcrypt** via `passlib`.
- On login, the username is returned as a token and used to authenticate the WebSocket connection.
- No external auth library or JWT is required.

---

## 💡 How It Works

1. A user registers with a username, email, and password.
2. On login, they connect to the WebSocket at `/ws/{username}`.
3. The server sends the full chat history on connection.
4. Messages sent by any user are broadcast to **all connected clients** in real time and saved to the database.

---

## 📌 Notes

- This project uses SQLite in **WAL (Write-Ahead Logging)** mode for better concurrent read/write performance.
- The app is intended for local/demo use. For production, consider adding proper session tokens (JWT), HTTPS, and a more robust database like PostgreSQL.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
