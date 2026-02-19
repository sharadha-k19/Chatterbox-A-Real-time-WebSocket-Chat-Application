import sqlite3
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from passlib.context import CryptContext
import uuid
from db import get_db_connection
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- MODELS ----------------

class RegisterUser(BaseModel):
    username: str
    email: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

# ---------------- CONNECTION MANAGER ----------------

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# ---------------- ROOT ----------------

@app.get("/")
def root():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(f.read())
    # ---------- Pydantic Models ----------

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

# ---------------- REGISTER ----------------

@app.post("/register")
def register(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        hashed = pwd_context.hash(user.password)

        cursor.execute(
            "INSERT INTO users (username,email,password_hash) VALUES (?,?,?)",
            (user.username, user.email, hashed)
        )

        conn.commit()

        return {"message": "User registered successfully"}

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")

    finally:
        conn.close()   # 🔥 THIS LINE IS VERY IMPORTANT

# ---------------- LOGIN ----------------

@app.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (user.username,)
        )

        db_user = cursor.fetchone()

        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        if not pwd_context.verify(user.password, db_user["password_hash"]):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        return {"token": db_user["username"]}

    finally:
        conn.close()   # 🔥 ALSO REQUIRED HERE

# ---------------- WEBSOCKET ----------------

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user from database
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if not user:
        await websocket.close()
        return

    # Send chat history
    cursor.execute("SELECT username, content FROM messages ORDER BY id ASC")
    history = cursor.fetchall()

    for msg in history:
        await websocket.send_text(f"{msg['username']}|||{msg['content']}")

    try:
        while True:
            data = await websocket.receive_text()

            cursor.execute(
                "INSERT INTO messages (user_id, username, content) VALUES (?, ?, ?)",
                (user["id"], user["username"], data)
            )
            conn.commit()

            await manager.broadcast(f"{user['username']}|||{data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    finally:
        conn.close()