#!/usr/bin/env python3
"""
Create session with provided verification code
"""
import asyncio
from telethon import TelegramClient

API_ID = 39967356
API_HASH = "6aea1aa164d582ea5b233a795673d4a5"
PHONE = "+37062838692"
CODE = "67755"
SESSION_NAME = "ipa_userbot_session"

async def create_session():
    """Create session with code"""
    print("Creating session with verification code...")
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    
    try:
        # Sign in with the code
        await client.sign_in(PHONE, CODE)
        
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
        
    except Exception as e:
        print(f"Error: {e}")
        
        # Check if 2FA is required
        if "password" in str(e).lower() or "2fa" in str(e).lower():
            print()
            print("⚠️  Two-factor authentication (2FA) is enabled on your account.")
            print("Please provide your 2FA password.")
            return False
        
        await client.disconnect()
        return False

if __name__ == "__main__":
    success = asyncio.run(create_session())
    exit(0 if success else 1)
