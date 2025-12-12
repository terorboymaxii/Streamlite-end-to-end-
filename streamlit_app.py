#!/usr/bin/env python3
import streamlit as st
import os
import time
import random
import json
import requests
import threading
import string
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Streamlit page config with full width
st.set_page_config(
    page_title="JACKSON E2E TOOL - Premium Multi-Task",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"  # No sidebar, full interface
)

# Global variables in session state
if 'bot_instances' not in st.session_state:
    st.session_state.bot_instances = {}
if 'viewing_task' not in st.session_state:
    st.session_state.viewing_task = None

# Same BotInstance class as before
class BotInstance:
    def __init__(self, task_id):
        self.task_id = task_id
        self.status = {
            "running": False,
            "current_action": "🤖 Bot Ready - Fill details and press START",
            "messages_sent": 0,
            "massages_sent": 0,
            "cycles_completed": 0,
            "errors": [],
            "console_logs": [],
            "verification_status": "❌ Not Verified",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_account": "None",
            "total_accounts": 0,
            "active_account_index": 0,
            "account_messages": {},
            "massage_method_used": True,
            "massage_success_rate": 0,
            "mode": "chat"
        }
        self.driver = None
        self.thread = None
        self.cookies_list = []
        self.current_cookie_index = 0
        self.account_messages = {}
        self.massage_attempts = 0
        self.massage_success = 0
        self.target_url = ""
        self.delay_seconds = 5
        self.total_cycles = 1
        
    def add_console_log(self, message, log_type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.status["console_logs"].append(log_entry)
        if len(self.status["console_logs"]) > 50:
            self.status["console_logs"] = self.status["console_logs"][-50:]
        
    def update_status(self, action, error=None):
        self.status["current_action"] = action
        self.add_console_log(action)
        
        if error:
            error_msg = f"ERROR: {error}"
            self.status["errors"].append(f"{datetime.now().strftime('%H:%M:%S')} - {error}")
            self.add_console_log(error_msg, "error")
            if len(self.status["errors"]) > 10:
                self.status["errors"] = self.status["errors"][-10:]

# Same FacebookFirefoxBot class (truncated for brevity, full class same as before)
class FacebookFirefoxBot:
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        self.driver = None
        self.mode = "chat"
        self.target_url = ""
        
    # ... (All the same methods as original Flask app)
    # check_authorization, get_device_key, setup_browser, etc.
    # YEH SAB WAHI CODE HAI JO APNE DIYA THA
    
    def run_bot_thread(self, cookie_content, message_content, target_url, delay_seconds, total_cycles, mode):
        # Same run_bot_thread method as original
        pass

# Generate task ID
def generate_task_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def create_bot_instance():
    task_id = generate_task_id()
    bot_instance = BotInstance(task_id)
    st.session_state.bot_instances[task_id] = bot_instance
    return task_id, bot_instance

def get_bot_instance(task_id):
    return st.session_state.bot_instances.get(task_id)

def stop_bot_instance(task_id):
    bot_instance = get_bot_instance(task_id)
    if bot_instance:
        bot_instance.status["running"] = False
        return True
    return False

# CSS for exact same styling as Flask app
st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    font-family: 'Courier New', monospace;
    background: #0d1117;
    color: #c9d1d9;
    margin: 0;
    padding: 20px;
}
.container {
    max-width: 1400px;
    margin: 0 auto;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    overflow: hidden;
}
.header {
    background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
    color: white;
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid #30363d;
}
.header h1 {
    font-size: 24px;
    margin-bottom: 5px;
}
.header .subtitle {
    font-size: 14px;
    opacity: 0.9;
}
.content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    padding: 20px;
}
@media (max-width: 768px) {
    .content {
        grid-template-columns: 1fr;
    }
}
.panel {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 20px;
}
.panel-title {
    color: #58a6ff;
    margin-bottom: 15px;
    font-size: 16px;
    font-weight: bold;
    border-bottom: 1px solid #30363d;
    padding-bottom: 10px;
}
.form-group {
    margin-bottom: 15px;
}
label {
    display: block;
    margin-bottom: 5px;
    color: #8b949e;
    font-size: 14px;
}
input, select {
    width: 100%;
    padding: 10px;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 4px;
    color: #c9d1d9;
    font-family: 'Courier New', monospace;
}
input:focus {
    border-color: #58a6ff;
    outline: none;
}
.btn {
    background: #238636;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
    margin: 5px 0;
    font-family: 'Courier New', monospace;
    font-weight: bold;
    transition: all 0.3s;
}
.btn:hover {
    background: #2ea043;
    transform: translateY(-1px);
}
.btn:disabled {
    background: #484f58;
    cursor: not-allowed;
    transform: none;
}
.btn-running {
    background: #da3633 !important;
}
.btn-stop {
    background: #da3633;
}
.btn-stop:hover {
    background: #f85149;
}
.btn-view {
    background: #8957e5;
}
.btn-view:hover {
    background: #986ee5;
}
.status-panel {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 15px;
}
.status-item {
    margin-bottom: 10px;
    padding: 8px;
    background: #161b22;
    border-radius: 4px;
    border-left: 3px solid #238636;
}
.status-verified {
    border-left-color: #3fb950;
}
.status-error {
    border-left-color: #f85149;
}
.status-warning {
    border-left-color: #d29922;
}
.console {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 15px;
    height: 400px;
    overflow-y: auto;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    white-space: pre-wrap;
    line-height: 1.4;
}
.log-entry {
    margin-bottom: 5px;
    padding: 3px 0;
    border-bottom: 1px solid #21262d;
    color: #58a6ff;
}
.stats {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-top: 15px;
}
.stat-item {
    background: #161b22;
    padding: 10px;
    border-radius: 4px;
    text-align: center;
    border: 1px solid #30363d;
}
.stat-number {
    font-size: 20px;
    font-weight: bold;
    color: #58a6ff;
}
.stat-label {
    font-size: 12px;
    color: #8b949e;
}
.file-input {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 4px;
    padding: 10px;
    color: #c9d1d9;
    width: 100%;
    margin-bottom: 10px;
}
.task-id-display {
    background: #161b22;
    padding: 15px;
    border-radius: 4px;
    margin: 10px 0;
    border: 1px solid #30363d;
    text-align: center;
}
.task-id {
    font-size: 24px;
    font-weight: bold;
    color: #58a6ff;
    letter-spacing: 2px;
}
.active-tasks {
    margin-top: 20px;
}
.task-item {
    background: #161b22;
    padding: 10px;
    margin: 5px 0;
    border-radius: 4px;
    border-left: 3px solid #238636;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.task-info {
    flex-grow: 1;
}
.task-actions {
    display: flex;
    gap: 5px;
}
.small-btn {
    padding: 5px 10px;
    font-size: 12px;
    width: auto;
}
.account-messages {
    margin-top: 10px;
    padding: 10px;
    background: #0d1117;
    border-radius: 4px;
    border: 1px solid #30363d;
}
.account-message-item {
    padding: 5px;
    margin: 2px 0;
    background: #161b22;
    border-radius: 2px;
    font-size: 11px;
}
.mode-selection {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 10px 0;
}
.mode-btn {
    padding: 10px;
    text-align: center;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
}
.mode-btn:hover {
    background: #30363d;
}
.mode-btn.active {
    background: #238636;
    border-color: #2ea043;
}
.massage-stats {
    background: #0d1117;
    border: 1px solid #8957e5;
    border-radius: 4px;
    padding: 10px;
    margin-top: 10px;
}
.massage-label {
    color: #986ee5;
    font-size: 12px;
}
.massage-value {
    color: #58a6ff;
    font-size: 16px;
    font-weight: bold;
}
.stTab {
    background-color: transparent !important;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    background-color: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent !important;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
}
.stTabs [aria-selected="true"] {
    background-color: #238636 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Main app interface - Exactly like Flask app
def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1>JACKSON E2E TOOL - PREMIUM MULTI-TASK</h1>
        <div class="subtitle">HATER'S | KI | MKC | JACKSON-BRAND UNBEATABLE</div>
        <div class="subtitle" style="color: #986ee5; margin-top: 5px;">🚀 MASSAGE SYSTEM: Complete Messages Sent At Once</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["⚙️ CONTROL PANEL", "📊 TASK STATUS", "🛠️ TASK MANAGEMENT"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### ⚙️ CONTROL PANEL")
            
            # Mode Selection
            col_mode1, col_mode2 = st.columns(2)
            with col_mode1:
                chat_active = st.button("💬 CHAT MODE", use_container_width=True, 
                                       type="primary" if st.session_state.get('mode', 'chat') == 'chat' else "secondary")
                if chat_active:
                    st.session_state.mode = 'chat'
            
            with col_mode2:
                comment_active = st.button("📝 COMMENT MODE", use_container_width=True,
                                          type="primary" if st.session_state.get('mode', 'chat') == 'comment' else "secondary")
                if comment_active:
                    st.session_state.mode = 'comment'
            
            current_mode = st.session_state.get('mode', 'chat')
            st.markdown(f"**Selected Mode:** {current_mode.upper()}")
            
            # File Uploaders
            cookie_file = st.file_uploader(
                "📁 COOKIE FILE (JSON - One JSON per line):",
                type=['json', 'txt'],
                help="Each line should contain a complete JSON cookie array"
            )
            
            message_file = st.file_uploader(
                "💬 MESSAGE FILE (TXT):",
                type=['txt'],
                help="Simple text file with one message per line"
            )
            
            # Target Input based on mode
            if current_mode == 'chat':
                target_url = st.text_input(
                    "🔗 FACEBOOK CHAT URL:",
                    placeholder="https://facebook.com/messages/t/..."
                )
            else:
                post_id = st.text_input(
                    "📝 FACEBOOK POST ID:",
                    placeholder="10000_7377373883",
                    help="Format: 10000_7377373883"
                )
                target_url = f"https://www.facebook.com/{post_id}" if post_id else ""
            
            # Configuration
            col_a, col_b = st.columns(2)
            with col_a:
                delay_seconds = st.number_input(
                    "⏱️ DELAY (SECONDS):",
                    min_value=2,
                    value=5,
                    step=1
                )
            
            with col_b:
                total_cycles = st.number_input(
                    "🔄 CYCLES (0=UNLIMITED):",
                    min_value=0,
                    value=1,
                    step=1
                )
            
            # Start Button
            if st.button("🚀 START NEW E2E (MASSAGE SYSTEM)", use_container_width=True, type="primary"):
                if cookie_file and message_file and target_url:
                    try:
                        cookie_content = cookie_file.getvalue().decode('utf-8')
                        message_content = message_file.getvalue().decode('utf-8')
                        
                        task_id, bot_instance = create_bot_instance()
                        
                        bot = FacebookFirefoxBot(bot_instance)
                        
                        def run_bot():
                            bot.run_bot_thread(
                                cookie_content, 
                                message_content, 
                                target_url, 
                                delay_seconds, 
                                total_cycles,
                                current_mode
                            )
                        
                        bot_instance.thread = threading.Thread(target=run_bot)
                        bot_instance.thread.daemon = True
                        bot_instance.thread.start()
                        
                        st.session_state.viewing_task = task_id
                        st.success(f"✅ E2E started with Task ID: **{task_id}**")
                        st.info(f"Mode: **{current_mode.upper()}** | Using **MASSAGE SYSTEM**")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                else:
                    st.error("❌ Please fill all required fields!")
        
        with col2:
            st.markdown("### 🛠️ QUICK TASK MANAGER")
            
            task_id_input = st.text_input(
                "🔍 ENTER TASK ID:",
                placeholder="Enter 7-digit Task ID",
                max_chars=7
            ).upper()
            
            col_manage1, col_manage2 = st.columns(2)
            with col_manage1:
                if st.button("👁️ VIEW CONSOLE", use_container_width=True):
                    if task_id_input and len(task_id_input) == 7:
                        bot_instance = get_bot_instance(task_id_input)
                        if bot_instance:
                            st.session_state.viewing_task = task_id_input
                            st.success(f"Now viewing console for Task: {task_id_input}")
                        else:
                            st.error("Task ID not found!")
            
            with col_manage2:
                if st.button("⏹️ STOP TASK", use_container_width=True, type="secondary"):
                    if task_id_input and len(task_id_input) == 7:
                        if stop_bot_instance(task_id_input):
                            st.success(f"Task {task_id_input} stopped successfully!")
                        else:
                            st.error("Task ID not found!")
            
            # Active Tasks List
            st.markdown("### 📋 ACTIVE TASKS")
            active_tasks = {k: v for k, v in st.session_state.bot_instances.items() if v.status["running"]}
            
            if not active_tasks:
                st.info("No active tasks")
            else:
                for task_id, instance in active_tasks.items():
                    with st.expander(f"Task {task_id} - {instance.status['current_account']}", expanded=False):
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        with col_stats1:
                            st.metric("Messages", instance.status['messages_sent'])
                        with col_stats2:
                            st.metric("Massage", instance.status['massages_sent'])
                        with col_stats3:
                            st.metric("Success", f"{instance.status['massage_success_rate']}%")
                        
                        if st.button(f"View & Stop {task_id}", key=f"view_{task_id}"):
                            st.session_state.viewing_task = task_id
                            st.rerun()
    
    with tab2:
        st.markdown("### 📊 TASK STATUS")
        
        # Task selection dropdown
        task_ids = list(st.session_state.bot_instances.keys())
        if task_ids:
            selected_task = st.selectbox(
                "Select Task to View:",
                task_ids,
                index=task_ids.index(st.session_state.viewing_task) if st.session_state.viewing_task in task_ids else 0
            )
            st.session_state.viewing_task = selected_task
        else:
            st.info("No tasks created yet")
            selected_task = None
        
        if selected_task and selected_task in st.session_state.bot_instances:
            bot_instance = st.session_state.bot_instances[selected_task]
            status = bot_instance.status
            
            # Task ID Display
            st.markdown(f"""
            <div class="task-id-display">
                <div>YOUR TASK ID:</div>
                <div class="task-id">{selected_task}</div>
                <div style="font-size: 12px; margin-top: 5px;">Use this ID to stop or view console</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Statistics
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.markdown("""
                <div class="stat-item">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">MESSAGES SENT</div>
                </div>
                """.format(status['messages_sent']), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="stat-item">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">MASSAGE SYSTEM</div>
                </div>
                """.format(status['massages_sent']), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="stat-item">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">CYCLES</div>
                </div>
                """.format(status['cycles_completed']), unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="stat-item">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">ACCOUNTS</div>
                </div>
                """.format(status['total_accounts']), unsafe_allow_html=True)
            
            with col5:
                st.markdown("""
                <div class="stat-item">
                    <div class="stat-number">{}%</div>
                    <div class="stat-label">SUCCESS RATE</div>
                </div>
                """.format(status['massage_success_rate']), unsafe_allow_html=True)
            
            with col6:
                st.markdown("""
                <div class="stat-item">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">CURRENT ACC</div>
                </div>
                """.format(status['active_account_index']), unsafe_allow_html=True)
            
            # Status Panel
            st.markdown("""
            <div class="status-panel">
                <div class="status-item">
                    <strong>VERIFICATION:</strong> <span id="verificationText">{}</span>
                </div>
                <div class="status-item">
                    <strong>STATUS:</strong> <span id="currentStatus">{}</span>
                </div>
                <div class="status-item">
                    <strong>ACTION:</strong> <span id="currentAction">{}</span>
                </div>
                <div class="status-item">
                    <strong>ACCOUNT:</strong> <span id="currentAccount">{}</span>
                </div>
                <div class="status-item">
                    <strong>MODE:</strong> <span id="currentMode">{}</span>
                </div>
            </div>
            """.format(
                status['verification_status'],
                '🟢 RUNNING' if status['running'] else '🔴 STOPPED',
                status['current_action'],
                status['current_account'],
                status['mode'].upper()
            ), unsafe_allow_html=True)
            
            # Account Messages
            if status['account_messages']:
                st.markdown("### 📨 ASSIGNED MESSAGES")
                for account, messages in status['account_messages'].items():
                    with st.expander(f"{account} - {len(messages)} messages"):
                        for msg in messages:
                            st.code(msg, language=None)
            
            # Console Output
            st.markdown("### 🖥️ CONSOLE OUTPUT")
            console_text = "\n".join(status['console_logs'][-30:]) if status['console_logs'] else "[SYSTEM] No console output yet"
            st.code(console_text, language="bash", line_numbers=True)
            
            # Auto-refresh if running
            if status['running']:
                st.rerun()
    
    with tab3:
        st.markdown("### 🛠️ ADVANCED TASK MANAGEMENT")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔍 TASK SEARCH")
            search_task_id = st.text_input(
                "Enter Task ID to manage:",
                placeholder="7-digit Task ID",
                max_chars=7
            ).upper()
            
            if search_task_id:
                bot_instance = get_bot_instance(search_task_id)
                if bot_instance:
                    st.success(f"Task **{search_task_id}** found!")
                    st.write(f"**Status:** {'🟢 Running' if bot_instance.status['running'] else '🔴 Stopped'}")
                    st.write(f"**Created:** {bot_instance.status['created_at']}")
                    st.write(f"**Messages Sent:** {bot_instance.status['messages_sent']}")
                    
                    if st.button(f"⏹️ STOP TASK {search_task_id}", use_container_width=True, type="secondary"):
                        stop_bot_instance(search_task_id)
                        st.success(f"Task {search_task_id} stopped!")
                        st.rerun()
                else:
                    st.error("Task not found!")
        
        with col2:
            st.markdown("#### 📊 ALL TASKS OVERVIEW")
            
            all_tasks = st.session_state.bot_instances
            if not all_tasks:
                st.info("No tasks created yet")
            else:
                for task_id, instance in all_tasks.items():
                    status_color = "🟢" if instance.status['running'] else "🔴"
                    st.write(f"{status_color} **{task_id}** - {instance.status['current_account']}")
                    st.progress(min(instance.status['messages_sent'] / 100, 1.0) if instance.status['messages_sent'] > 0 else 0)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #8b949e; font-size: 12px;">
        <p>JACKSON BRAND E2E TOOL - Premium Multi-Task | MASSAGE SYSTEM | Contact: +923481981346</p>
        <p>Each line in cookie file = one Facebook account | Each account gets specific messages</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
