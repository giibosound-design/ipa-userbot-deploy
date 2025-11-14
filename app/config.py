"""
Configuration for Telethon IPA Patcher Userbot
"""
import os

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "39967356"))
API_HASH = os.getenv("API_HASH", "6aea1aa164d582ea5b233a795673d4a5")

# User phone number
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "+37062838692")

# Session configuration
SESSION_NAME = "ipa_userbot_session"
SESSION_FILE = f"{SESSION_NAME}.session"

# File paths
TEMP_DIR = "/tmp/ipa_bot"
DYLIB_PATH = "blatantsPatch.dylib"
IPAPATCH_BINARY = "./tools/ipapatch/ipapatch"

# Bot settings
COMMAND_PREFIX = "."  # Commands start with . (e.g., .patch)
SESSION_TIMEOUT = 3600  # 1 hour
MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4GB

# Server configuration (for health monitoring)
HEALTH_PORT = int(os.getenv("PORT", "8080"))
HOST = "0.0.0.0"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
