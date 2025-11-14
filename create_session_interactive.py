#!/usr/bin/env python3
"""
Interactive session creation for Telethon userbot
"""
import asyncio
import sys
from telethon import TelegramClient

API_ID = 39967356
API_HASH = "6aea1aa164d582ea5b233a795673d4a5"
PHONE = "+37062838692"
SESSION_NAME = "ipa_userbot_session"

async def create_session():
    """Create Telethon session interactively"""
    print("=" * 70)
    print("TELEGRAM SESSION CREATION")
    print("=" * 70)
    print()
    print(f"Sending verification code to: {PHONE}")
    print()
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE)
        print("✓ Verification code sent to your Telegram app!")
        print()
        
        # This will prompt for code
        await client.start(phone=PHONE)
    
    me = await client.get_me()
    
    print()
    print("=" * 70)
    print("✅ SESSION CREATED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print(f"Name: {me.first_name} {me.last_name or ''}")
    print(f"Phone: {me.phone}")
    print(f"Username: @{me.username}" if me.username else "Username: None")
    print(f"Premium: {'Yes ✅' if me.premium else 'No'}")
    print()
    print(f"Session file: {SESSION_NAME}.session")
    print()
    print("=" * 70)
    
    await client.disconnect()
    return True

if __name__ == "__main__":
    try:
        asyncio.run(create_session())
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)
