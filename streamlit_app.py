import streamlit as st
import time
import threading
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests
import os

st.set_page_config(
    page_title="Mr. JackSon E2E",
    page_icon="ðŸ’™",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Background Image */
    .stApp {
        background-image: url('https://i.postimg.cc/90Tg7ngL/228248c95e06fd0bf5da9241cf7a4886.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main .block-container {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 32px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: 0.3s;
}
.main .block-container:hover {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}
    
    .main-header {
    background: rgba(0, 0, 0, 0.7);
    background-image: url("https://i.postimg.cc/Zq4ZMNyz/546c121c192e6a7a8e88bec385d375d5.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    backdrop-filter: blur(12px) brightness(0.9);
    -webkit-backdrop-filter: blur(12px) brightness(0.9);
    padding: 2rem;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
}

/* Optional: Overlay for extra softness */
.main-header::before {
    content: "";
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.6); /* Darker overlay */
    border-radius: 18px;
    z-index: 0;
}

.main-header h1, 
.main-header p {
    position: relative;
    z-index: 1;
    color: #fff;
}
    
    .main-header h1 {
        background: linear-gradient(45deg, #1e90ff, #00bfff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .prince-logo {
    width: 80px;
    height: 80px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 2px solid #1e90ff;
    box-shadow: 0 4px 10px rgba(30, 144, 255, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.prince-logo:hover {
    transform: scale(1.08);
    box-shadow: 0 6px 14px rgba(30, 144, 255, 0.6);
}
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #1e90ff, #00bfff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30, 144, 255, 0.4);
        width: 100%;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 144, 255, 0.6);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 8px;
        color: white;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        background: rgba(255, 255, 255, 0.2);
        border-color: #1e90ff;
        box-shadow: 0 0 0 2px rgba(30, 144, 255, 0.2);
        color: white;
    }
    
    /* Labels */
    label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.06);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #1e90ff, #00bfff);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #1e90ff;
        font-weight: 700;
        font-size: 1.8rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
    }
    
    /* Console Section */
    .console-section {
        margin-top: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        border: 1px solid rgba(30, 144, 255, 0.3);
    }
    
    .console-header {
        color: #1e90ff;
        text-shadow: 0 0 10px rgba(30, 144, 255, 0.5);
        margin-bottom: 20px;
        font-weight: 600;
    }
    
    .console-output {
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(30, 144, 255, 0.4);
        border-radius: 10px;
        padding: 12px;
        font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
        font-size: 12px;
        color: #00ff88;
        line-height: 1.6;
        max-height: 400px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: rgba(30, 144, 255, 0.5) rgba(0, 0, 0, 0.2);
    }
    
    .console-output::-webkit-scrollbar {
        width: 8px;
    }
    
    .console-output::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    
    .console-output::-webkit-scrollbar-thumb {
        background: rgba(30, 144, 255, 0.5);
        border-radius: 4px;
    }
    
    .console-output::-webkit-scrollbar-thumb:hover {
        background: rgba(30, 144, 255, 0.7);
    }
    
    .console-line {
        margin-bottom: 3px;
        word-wrap: break-word;
        padding: 6px 10px;
        padding-left: 28px;
        color: #00ff88;
        background: rgba(30, 144, 255, 0.08);
        border-left: 2px solid rgba(30, 144, 255, 0.4);
        position: relative;
    }
    
    .console-line::before {
        content: 'â–º';
        position: absolute;
        left: 10px;
        opacity: 0.6;
        color: #1e90ff;
    }
    
    /* Success/Error Boxes */
    .success-box {
        background: linear-gradient(135deg, #1e90ff 0%, #00bfff 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Info Card */
    .info-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        margin-top: 3rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
    
    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state)
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', automation_state)
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector {idx+1}/{len(message_input_selectors)} "{selector[:50]}..." found {len(elements)} elements', automation_state)
            
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        log_message(f'{process_id}: Found editable element with selector #{idx+1}', automation_state)
                        
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}: âœ… Found message input with text: {element_text[:50]}', automation_state)
                            return element
                        elif idx < 10:
                            log_message(f'{process_id}: âœ… Using primary selector editable element (#{idx+1})', automation_state)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}: âœ… Using fallback editable element', automation_state)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed: {str(e)[:50]}', automation_state)
                    continue
        except Exception as e:
            continue
    
    try:
        page_source = driver.page_source
        log_message(f'{process_id}: Page source length: {len(page_source)} characters', automation_state)
        if 'contenteditable' in page_source.lower():
            log_message(f'{process_id}: Page contains contenteditable elements', automation_state)
        else:
            log_message(f'{process_id}: No contenteditable elements found in page', automation_state)
    except Exception:
        pass
    
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state)
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state)
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', automation_state)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', automation_state)
        
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'
    
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state)
        driver = setup_browser(automation_state)
        
        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config['cookies'] and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state)
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'{process_id}: Opening messages...', automation_state)
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(15)
        
        message_input = find_message_input(driver, process_id, automation_state)
        
        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
        
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello!']
        
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
            
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
            
            try:
                # Clear the input first
                driver.execute_script("""
                    const element = arguments[0];
                    element.focus();
                    element.click();
                    
                    if (element.tagName === 'DIV') {
                        element.textContent = '';
                        element.innerHTML = '';
                    } else {
                        element.value = '';
                    }
                    
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                """, message_input)
                
                time.sleep(0.5)
                
                # Type the message character by character (more realistic)
                for char in message_to_send:
                    driver.execute_script("""
                        const element = arguments[0];
                        const char = arguments[1];
                        
                        if (element.tagName === 'DIV') {
                            element.textContent += char;
                            element.innerHTML += char;
                        } else {
                            element.value += char;
                        }
                        
                        element.dispatchEvent(new InputEvent('input', { 
                            bubbles: true, 
                            data: char 
                        }));
                    """, message_input, char)
                    time.sleep(0.05)  # Small delay between characters
                
                time.sleep(1)
                
                # Try multiple methods to send
                send_methods = [
                    # Method 1: Send button
                    """
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i], [data-testid="send-button"], [aria-label*="send" i]');
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null && btn.getBoundingClientRect().width > 0) {
                            btn.click();
                            return 'send_button_clicked';
                        }
                    }
                    return 'no_send_button';
                    """,
                    
                    # Method 2: Enter key
                    """
                    const element = arguments[0];
                    const enterEvent = new KeyboardEvent('keydown', {
                        key: 'Enter',
                        code: 'Enter',
                        keyCode: 13,
                        which: 13,
                        bubbles: true
                    });
                    element.dispatchEvent(enterEvent);
                    
                    const enterUp = new KeyboardEvent('keyup', {
                        key: 'Enter',
                        code: 'Enter',
                        keyCode: 13,
                        which: 13,
                        bubbles: true
                    });
                    element.dispatchEvent(enterUp);
                    return 'enter_key_pressed';
                    """,
                    
                    # Method 3: Form submission
                    """
                    const element = arguments[0];
                    let form = element;
                    while (form && form.tagName !== 'FORM') {
                        form = form.parentElement;
                    }
                    if (form) {
                        form.submit();
                        return 'form_submitted';
                    }
                    return 'no_form';
                    """
                ]
                
                message_sent = False
                for method_idx, method in enumerate(send_methods):
                    try:
                        result = driver.execute_script(method, message_input)
                        log_message(f'{process_id}: Send method {method_idx + 1} result: {result}', automation_state)
                        
                        if 'clicked' in result or 'pressed' in result or 'submitted' in result:
                            message_sent = True
                            break
                    except Exception as e:
                        log_message(f'{process_id}: Send method {method_idx + 1} failed: {str(e)[:50]}', automation_state)
                        continue
                
                if not message_sent:
                    # Final fallback: direct Enter key simulation
                    try:
                        from selenium.webdriver.common.keys import Keys
                        message_input.send_keys(Keys.ENTER)
                        log_message(f'{process_id}: Using Selenium Enter key fallback', automation_state)
                        message_sent = True
                    except Exception as e:
                        log_message(f'{process_id}: Enter key fallback failed: {str(e)}', automation_state)
                
                time.sleep(2)  # Wait for message to be sent
                
                if message_sent:
                    messages_sent += 1
                    automation_state.message_count = messages_sent
                    log_message(f'{process_id}: âœ… Message {messages_sent} sent: {message_to_send[:30]}...', automation_state)
                else:
                    log_message(f'{process_id}: âŒ Failed to send message', automation_state)
                
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'{process_id}: Error sending message: {str(e)}', automation_state)
                # Try to find message input again
                message_input = find_message_input(driver, process_id, automation_state)
                if not message_input:
                    log_message(f'{process_id}: Lost message input, stopping...', automation_state)
                    break
        
        log_message(f'{process_id}: Automation stopped! Total messages sent: {messages_sent}', automation_state)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return messages_sent
        
    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state)
            except:
                pass
                                                
def run_automation_with_notification(user_config, username, automation_state, user_id):
    """First send admin notification, then start automation"""
    send_admin_notification(user_config, username, automation_state, user_id)
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    
    db.set_automation_running(user_id, True)
    
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

# Updated header with Mr. JackSon E2E branding
st.markdown('<style>.main-header h1{margin-top:15px;}</style><div class="main-header"><img src="https://i.postimg.cc/9fpZqGjn/17adef215d4766a8620c99e8a17227b5.jpg" class="prince-logo"><h1>Mr. JackSon E2E<br>AUTOMATION SYSTEM</h1></div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["ðŸ” Login", "âœ¨ Sign Up"])
    
    with tab1:
        st.markdown("### Welcome to Mr. JackSon E2E!")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    
                    should_auto_start = db.get_automation_running(user_id)
                    if should_auto_start:
                        user_config = db.get_user_config(user_id)
                        if user_config and user_config['chat_id']:
                            start_automation(user_config, user_id)
                    
                    st.success(f"âœ… Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("âŒ Invalid username or password!")
            else:
                st.warning("âš ï¸ Please enter both username and password")
    
    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"âœ… {message} Please login now!")
                    else:
                        st.error(f"âŒ {message}")
                else:
                    st.error("âŒ Passwords do not match!")
            else:
                st.warning("âš ï¸ Please fill all fields")

else:
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
    
    st.sidebar.markdown(f"### ðŸ‘¤ {st.session_state.username}")
    st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
    
    if st.sidebar.button("ðŸšª Logout", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
        
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.automation_running = False
        st.session_state.auto_start_checked = False
        st.rerun()
    
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["âš™ï¸ Configuration", "ðŸš€ Automation"])
        
        with tab1:
            st.markdown("### Your Configuration")
            
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'], 
                                   placeholder="e.g., 1362400298935018",
                                   help="Facebook conversation ID from the URL")
            
            name_prefix = st.text_input("Name Prefix", value=user_config['name_prefix'],
                                       placeholder="e.g., [Mr. JackSon E2E]",
                                       help="Prefix to add before each message")
            
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, 
                                   value=user_config['delay'],
                                   help="Wait time between messages")
            
            cookies = st.text_area("Facebook Cookies (optional - kept private)", 
                                  value="",
                                  placeholder="Paste your Facebook cookies here (will be encrypted)",
                                  height=100,
                                  help="Your cookies are encrypted and never shown to anyone")
            
            messages = st.text_area("Messages (one per line)", 
                                   value=user_config['messages'],
                                   placeholder="Type your messages here, one per line",
                                   height=150,
                                   help="Enter each message on a new line")
            
            if st.button("ðŸ’¾ Save Configuration", use_container_width=True):
                final_cookies = cookies if cookies.strip() else user_config['cookies']
                db.update_user_config(
                    st.session_state.user_id,
                    chat_id,
                    name_prefix,
                    delay,
                    final_cookies,
                    messages
                )
                st.success("âœ… Configuration saved successfully!")
                st.rerun()
        
        with tab2:
            st.markdown("### Automation Control")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            
            with col2:
                status = "ðŸŸ¢ Running" if st.session_state.automation_state.running else "ðŸ”´ Stopped"
                st.metric("Status", status)
            
            with col3:
                st.metric("Total Logs", len(st.session_state.automation_state.logs))
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("â–¶ï¸ Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                    current_config = db.get_user_config(st.session_state.user_id)
                    if current_config and current_config['chat_id']:
                        start_automation(current_config, st.session_state.user_id)
                        st.rerun()
                    else:
                        st.error("âŒ Please configure Chat ID first!")
            
            with col2:
                if st.button("â¹ï¸ Stop Automation", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.rerun()
            
            st.markdown('<div class="console-section"><h4 class="console-header"><i class="fas fa-terminal"></i> Live Console Monitor</h4></div>', unsafe_allow_html=True)
            
            if st.session_state.automation_state.logs:
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-50:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)
            else:
                st.markdown('<div class="console-output"><div class="console-line">ðŸš€ Console ready... Start automation to see logs here.</div></div>', unsafe_allow_html=True)
            
            if st.session_state.automation_state.running:
                time.sleep(1)
                st.rerun()

st.markdown('<div class="footer"> Mr. JackSon E2E Automation System <br>All Rights Reserved</div>', unsafe_allow_html=True)
