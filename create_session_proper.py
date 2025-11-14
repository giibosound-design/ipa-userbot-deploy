#!/usr/bin/env python3
"""
Create session properly with code
"""
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

API_ID = 39967356
API_HASH = "6aea1aa164d582ea5b233a795673d4a5"
PHONE = "+37062838692"
CODE = "67755"
SESSION_NAME = "ipa_userbot_session"

async def create_session():
    """Create session"""
    print("Creating Telegram session...")
    print()
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        # Send code request
        sent_code = await client.send_code_request(PHONE)
        
        try:
            # Try to sign in with the code
            await client.sign_in(PHONE, CODE, phone_code_hash=sent_code.phone_code_hash)
            
        except SessionPasswordNeededError:
            print()
            print("⚠️  Two-factor authentication (2FA) is enabled.")
            print("Please enter your 2FA password:")
            password = input("Password: ")
            await client.sign_in(password=password)
    
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
    print(f"User ID: {me.id}")
    print()
    print(f"Session file created: {SESSION_NAME}.session")
    print()
    print("=" * 70)
    
    await client.disconnect()
    return True

if __name__ == "__main__":
    try:
        success = asyncio.run(create_session())
        exit(0 if success else 1)
    except Exception as e:
        print(f"\nError: {e}")
        exit(1)
