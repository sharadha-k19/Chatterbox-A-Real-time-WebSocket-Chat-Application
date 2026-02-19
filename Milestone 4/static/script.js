let isRegisterMode = false;
let socket = null;
let currentUser = "";

// Toggle between Login and Register
function toggleMode() {
    isRegisterMode = !isRegisterMode;

    const button = document.getElementById("authButton");
    const toggleText = document.querySelector(".toggle");
    const emailInput = document.getElementById("email");

    if (isRegisterMode) {
        button.innerText = "Register";
        toggleText.innerText = "Already have an account? Login";
        emailInput.style.display = "block";
    } else {
        button.innerText = "Login";
        toggleText.innerText = "Don't have an account? Register";
        emailInput.style.display = "none";
    }
}

// Handle Register / Login
async function handleAuth() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Please fill all required fields");
        return;
    }

    if (isRegisterMode) {
        // REGISTER
        const response = await fetch("/register", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ Registration successful! Now login.");
            toggleMode();
        } else {
            alert("❌ " + data.detail);
        }

    } else {
        // LOGIN
        const response = await fetch("/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = username;

            document.getElementById("authSection").style.display = "none";
            document.getElementById("chatSection").style.display = "block";

            connectWebSocket(data.token);
        } else {
            alert("❌ " + data.detail);
        }
    }
}

// Connect WebSocket
function connectWebSocket(token) {
    socket = new WebSocket(`ws://localhost:8000/ws/${token}`);

    socket.onmessage = function(event) {
        const data = event.data;
        const parts = data.split("|||");
    
        const sender = parts[0];
        const message = parts[1];
    
        if (sender === currentUser) {
            addMessage(message, "self");
        } else {
            addMessage(sender + ": " + message, "other");
        }
    };
}

// Send Message
function sendMessage() {
    const messageInput = document.getElementById("message");
    const message = messageInput.value;

    if (message.trim() === "") return;

    socket.send(message);
    messageInput.value = "";
}
// Add message to chat UI
function addMessage(text, type) {
    const chat = document.getElementById("chat");

    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", type);

    msgDiv.innerText = text;

    chat.appendChild(msgDiv);

    chat.scrollTop = chat.scrollHeight;
}