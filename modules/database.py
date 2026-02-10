import sqlite3
import hashlib
import os
from datetime import datetime
import json

DB_FILE = "english_learning_db/users_chat.db"

def init_db():
    """Initialize the database with necessary tables."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Users table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')

    # Check if email column exists (for migration)
    try:
        c.execute('SELECT email FROM users LIMIT 1')
    except sqlite3.OperationalError:
        c.execute('ALTER TABLE users ADD COLUMN email TEXT')
    
    # Conversations table
    c.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Messages table
    c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        is_voice BOOLEAN DEFAULT 0,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, email=None):
    """Create a new user."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        password_hash = hash_password(password)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('INSERT INTO users (username, password_hash, email, created_at) VALUES (?, ?, ?, ?)',
                  (username, password_hash, email, created_at))
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Username or Email already exists"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    password_hash = hash_password(password)
    c.execute('SELECT id, username FROM users WHERE username = ? AND password_hash = ?', 
              (username, password_hash))
    user = c.fetchone()
    conn.close()
    return user # Returns (id, username) or None

def create_conversation(user_id, title="New Conversation"):
    """Create a new conversation for a user."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO conversations (user_id, title, created_at) VALUES (?, ?, ?)',
              (user_id, title, created_at))
    chat_id = c.lastrowid
    conn.commit()
    conn.close()
    return chat_id

def get_user_conversations(user_id):
    """Get all conversations for a user."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, title, created_at FROM conversations WHERE user_id = ? ORDER BY id DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    
    conversations = []
    for row in rows:
        conversations.append({
            "id": row[0],
            "title": row[1],
            "created_at": row[2]
        })
    return conversations

def save_message(conversation_id, role, content, is_voice=False):
    """Save a message to a conversation."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%H:%M")
    c.execute('''
    INSERT INTO messages (conversation_id, role, content, timestamp, is_voice) 
    VALUES (?, ?, ?, ?, ?)
    ''', (conversation_id, role, content, timestamp, is_voice))
    conn.commit()
    conn.close()

def get_conversation_messages(conversation_id):
    """Get all messages for a conversation."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
    SELECT role, content, timestamp, is_voice 
    FROM messages 
    WHERE conversation_id = ? 
    ORDER BY id ASC
    ''', (conversation_id,))
    rows = c.fetchall()
    conn.close()
    
    messages = []
    for row in rows:
        messages.append({
            "role": row[0],
            "content": row[1],
            "timestamp": row[2],
            "voice": bool(row[3])
        })
    return messages

def delete_conversation(conversation_id):
    """Delete a conversation and its messages."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
    c.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
    conn.commit()
    conn.close()
