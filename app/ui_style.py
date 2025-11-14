"""
UI Style Module - Professional Templates and Design
"""

# Emojis
EMOJI = {
    'robot': '🤖',
    'patch': '🔧',
    'status': '📊',
    'help': 'ℹ️',
    'clear': '🗑️',
    'settings': '⚙️',
    'about': '📖',
    'back': '◀️',
    'menu': '🏠',
    'download': '📥',
    'upload': '📤',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'file': '📱',
    'size': '📦',
    'processing': '⏳',
    'premium': '💎',
    'free': '🆓',
}

# Separators
SEP_THICK = '═' * 30
SEP_THIN = '─' * 30
SEP_DOT = '· ' * 15

# Headers
def header(text: str, emoji: str = '') -> str:
    """Create a header with emoji"""
    if emoji:
        return f"\n{emoji} **{text}** {emoji}\n{SEP_THICK}\n"
    return f"\n**{text}**\n{SEP_THICK}\n"

def subheader(text: str) -> str:
    """Create a subheader"""
    return f"\n**{text}**\n{SEP_THIN}\n"

# Main Menu
MAIN_MENU = f"""
{EMOJI['robot']} **IPA Patcher Bot**
{SEP_THICK}

Welcome! I can patch IPA files with blatantsPatch.dylib.

**Features:**
{EMOJI['patch']} Automatic IPA patching
{EMOJI['premium']} 4GB file support (Premium)
{EMOJI['upload']} Fast upload/download speeds
{EMOJI['status']} Real-time progress tracking

**How to use:**
1. Upload or forward an IPA file
2. Click '{EMOJI['patch']} Patch IPA' button
3. Download your patched IPA!

{SEP_THIN}
Choose an option below:
"""

# Help Text
HELP_TEXT = f"""
{EMOJI['help']} **Help & Commands**
{SEP_THICK}

**Commands:**
/start - Show main menu
/menu - Return to main menu
/help - Show this help
/status - Show bot status
/clear - Clear all messages and reset

**How to patch IPA:**
1️⃣ Upload an IPA file (up to 4GB)
   • Direct upload
   • Forward from another chat
   • Forward from channel

2️⃣ Click the '{EMOJI['patch']} Patch IPA' button

3️⃣ Wait for processing
   • Progress bar will show
   • Takes 1-5 minutes

4️⃣ Download your patched IPA
   • Sent back to you automatically
   • Ready to install

**Supported files:**
{EMOJI['file']} .ipa - iOS applications
{EMOJI['file']} .deb - Debian packages
{EMOJI['file']} .dylib - Dynamic libraries

**Features:**
{EMOJI['success']} 4GB file support
{EMOJI['success']} Fast upload/download
{EMOJI['success']} Progress bars
{EMOJI['success']} Automatic cleanup
{EMOJI['success']} Forwarded files supported

{SEP_THIN}
Need more help? Check /status for bot info.
"""

# Status Template
def status_text(user_info: dict, file_count: int = 0) -> str:
    """Generate status text"""
    return f"""
{EMOJI['status']} **Bot Status**
{SEP_THICK}

**User Information:**
Name: {user_info.get('name', 'Unknown')}
Username: @{user_info.get('username', 'none')}
Premium: {EMOJI['premium'] if user_info.get('premium') else EMOJI['free']} {'Yes' if user_info.get('premium') else 'No'}
4GB Support: {EMOJI['success'] if user_info.get('premium') else EMOJI['error']} {'Enabled' if user_info.get('premium') else 'Limited to 2GB'}

**Bot Status:**
Session: {EMOJI['success']} Active
Files in queue: {file_count}
Bot: {EMOJI['success']} Running

{SEP_THIN}
All systems operational!
"""

# Settings Template
SETTINGS_TEXT = f"""
{EMOJI['settings']} **Settings**
{SEP_THICK}

**Current Configuration:**
Auto-delete: {EMOJI['success']} Enabled
Progress bars: {EMOJI['success']} Enabled
Notifications: {EMOJI['success']} Enabled

**File Management:**
Max file size: 4GB (Premium)
Auto-cleanup: {EMOJI['success']} Enabled
Temp storage: /tmp/ipa_bot

{SEP_THIN}
Settings are optimized for best performance.
"""

# About Template
ABOUT_TEXT = f"""
{EMOJI['about']} **About IPA Patcher Bot**
{SEP_THICK}

**Version:** 2.0.0
**Type:** Telethon Userbot
**Platform:** Fly.io

**Features:**
{EMOJI['patch']} IPA patching with blatantsPatch.dylib
{EMOJI['premium']} 4GB file support (Telegram Premium)
{EMOJI['upload']} Fast upload/download speeds
{EMOJI['status']} Real-time progress tracking
{EMOJI['success']} Single-window UI
{EMOJI['success']} Forwarded files support

**Tools Used:**
• ipapatch (Go binary)
• pyzule-rw (Python)
• blatantsPatch.dylib

**Repository:**
github.com/giibosound-design/ipa-userbot-deploy

{SEP_THIN}
Made with {EMOJI['robot']} by Manus AI
"""

# Download Progress Template
def download_progress_text(filename: str, size: str, percent: int = 0) -> str:
    """Generate download progress text"""
    bar_length = 20
    filled = int(bar_length * percent / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    return f"""
{EMOJI['download']} **Downloading File**
{SEP_THIN}

{EMOJI['file']} File: {filename}
{EMOJI['size']} Size: {size}

Progress: {percent}%
[{bar}]

{EMOJI['processing']} Please wait...
"""

# Upload Progress Template
def upload_progress_text(filename: str, size: str, percent: int = 0) -> str:
    """Generate upload progress text"""
    bar_length = 20
    filled = int(bar_length * percent / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    return f"""
{EMOJI['upload']} **Uploading Patched IPA**
{SEP_THIN}

{EMOJI['file']} File: {filename}
{EMOJI['size']} Size: {size}

Progress: {percent}%
[{bar}]

{EMOJI['processing']} Almost done...
"""

# Patching Progress Template
def patching_progress_text(filename: str, size: str) -> str:
    """Generate patching progress text"""
    return f"""
{EMOJI['patch']} **Patching IPA**
{SEP_THIN}

{EMOJI['file']} File: {filename}
{EMOJI['size']} Size: {size}

{EMOJI['processing']} Processing...
This may take a few minutes...

**Steps:**
1. {EMOJI['success']} Extracting IPA
2. {EMOJI['processing']} Injecting dylib
3. ⏸️ Repackaging
4. ⏸️ Signing

Please wait...
"""

# Success Template
def success_text(filename: str, size: str) -> str:
    """Generate success message"""
    return f"""
{EMOJI['success']} **IPA Patched Successfully!**
{SEP_THICK}

{EMOJI['file']} Output: {filename}
{EMOJI['size']} Size: {size}

{EMOJI['success']} Patched with blatantsPatch.dylib
{EMOJI['success']} Ready to install!

{SEP_THIN}
Your patched IPA has been sent above.
"""

# Error Template
def error_text(error_msg: str) -> str:
    """Generate error message"""
    return f"""
{EMOJI['error']} **Error Occurred**
{SEP_THIN}

{error_msg[:200]}

{EMOJI['warning']} Please try again or upload a different file.

{SEP_THIN}
Use /menu to return to main menu.
"""

# File Received Template
def file_received_text(filename: str, size: str, forwarded: bool = False) -> str:
    """Generate file received message"""
    source = "forwarded" if forwarded else "uploaded"
    return f"""
{EMOJI['success']} **File Received!**
{SEP_THIN}

{EMOJI['file']} File: {filename}
{EMOJI['size']} Size: {size}
{EMOJI['download']} Source: {source.capitalize()}

{EMOJI['success']} Download complete!

{SEP_THIN}
Click '{EMOJI['patch']} Patch IPA' to start patching.
"""

# Clear Confirmation
CLEAR_CONFIRM_TEXT = f"""
{EMOJI['warning']} **Clear All Messages?**
{SEP_THIN}

This will:
{EMOJI['clear']} Delete all messages in this chat
{EMOJI['clear']} Remove all uploaded files
{EMOJI['clear']} Reset all settings
{EMOJI['clear']} Start fresh

{EMOJI['warning']} This action cannot be undone!

{SEP_THIN}
Are you sure?
"""

# Cleared Text
CLEARED_TEXT = f"""
{EMOJI['success']} **Chat Cleared!**
{SEP_THIN}

All messages and files have been removed.
Starting fresh...

{SEP_THIN}
Welcome back! Upload a file to get started.
"""
