import sqlite3
import json
import os
import hashlib
from pathlib import Path

# Database file path - Render compatible
if 'RENDER' in os.environ:
    DB_PATH = '/tmp/e2ee_database.db'
else:
    DB_PATH = 'e2ee_database.db'

def get_db_connection():
    """Get database connection with proper error handling for Render"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        # Try alternative path
        try:
            DB_PATH_ALT = './e2ee_database.db'
            conn = sqlite3.connect(DB_PATH_ALT)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e2:
            print(f"Alternative database connection also failed: {e2}")
            raise e

def init_db():
    """Initialize database tables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # User configurations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_configs (
                user_id INTEGER PRIMARY KEY,
                chat_id TEXT,
                name_prefix TEXT,
                delay INTEGER DEFAULT 30,
                cookies TEXT,
                messages TEXT,
                automation_running BOOLEAN DEFAULT FALSE,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Admin E2EE thread IDs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_threads (
                user_id INTEGER PRIMARY KEY,
                thread_id TEXT NOT NULL,
                cookies TEXT,
                chat_type TEXT DEFAULT 'REGULAR',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Create new user account"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        
        user_id = cursor.lastrowid
        
        # Create default configuration for user
        cursor.execute(
            'INSERT INTO user_configs (user_id, chat_id, name_prefix, delay, cookies, messages) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, '', '[END TO END]', 30, '', 'Hello!\nHow are you?')
        )
        
        conn.commit()
        conn.close()
        
        return True, f"User {username} created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists!"
    except Exception as e:
        return False, f"Error creating user: {str(e)}"

def verify_user(username, password):
    """Verify user credentials"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute(
            'SELECT id FROM users WHERE username = ? AND password_hash = ? AND is_active = TRUE',
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result['id'] if result else None
    except Exception as e:
        print(f"User verification error: {e}")
        return None

def get_user_config(user_id):
    """Get user configuration"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT chat_id, name_prefix, delay, cookies, messages FROM user_configs WHERE user_id = ?',
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'chat_id': result['chat_id'],
                'name_prefix': result['name_prefix'],
                'delay': result['delay'],
                'cookies': result['cookies'],
                'messages': result['messages']
            }
        else:
            # Return default config if not found
            return {
                'chat_id': '',
                'name_prefix': '[END TO END]',
                'delay': 30,
                'cookies': '',
                'messages': 'Hello!\nHow are you?'
            }
    except Exception as e:
        print(f"Get user config error: {e}")
        return {
            'chat_id': '',
            'name_prefix': '[END TO END]',
            'delay': 30,
            'cookies': '',
            'messages': 'Hello!\nHow are you?'
        }

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    """Update user configuration"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT OR REPLACE INTO user_configs 
               (user_id, chat_id, name_prefix, delay, cookies, messages, updated_at) 
               VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)''',
            (user_id, chat_id, name_prefix, delay, cookies, messages)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Update user config error: {e}")
        return False

def get_automation_running(user_id):
    """Check if automation is running for user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT automation_running FROM user_configs WHERE user_id = ?',
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result['automation_running'] if result else False
    except Exception as e:
        print(f"Get automation running error: {e}")
        return False

def set_automation_running(user_id, running):
    """Set automation running status"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE user_configs SET automation_running = ? WHERE user_id = ?',
            (running, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Set automation running error: {e}")
        return False

def get_username(user_id):
    """Get username from user ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT username FROM users WHERE id = ?',
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result['username'] if result else 'Unknown User'
    except Exception as e:
        print(f"Get username error: {e}")
        return 'Unknown User'

def set_admin_e2ee_thread_id(user_id, thread_id, cookies, chat_type='REGULAR'):
    """Set admin E2EE thread ID for user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT OR REPLACE INTO admin_threads 
               (user_id, thread_id, cookies, chat_type, created_at) 
               VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)''',
            (user_id, thread_id, cookies, chat_type)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Set admin thread ID error: {e}")
        return False

def get_admin_e2ee_thread_id(user_id):
    """Get admin E2EE thread ID for user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT thread_id FROM admin_threads WHERE user_id = ?',
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result['thread_id'] if result else None
    except Exception as e:
        print(f"Get admin thread ID error: {e}")
        return None

def cleanup_old_sessions():
    """Clean up old sessions and inactive users"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # You can add cleanup logic here if needed
        # For example, delete users older than X days who never activated
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Cleanup error: {e}")
        return False

# Initialize database when module is imported
init_db()
