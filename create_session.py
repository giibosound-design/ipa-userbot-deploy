#!/usr/bin/env python3
"""
Session creation script for Telethon userbot
This script creates a permanent session file that can be reused
"""
import asyncio
import sys
from telethon import TelegramClient
from app import config

async def create_session():
    """Create Telethon session with phone verification"""
    print("=" * 70)
    print("IPA PATCHER USERBOT - SESSION CREATION")
    print("=" * 70)
    print()
    print("This will create a permanent session for your Telegram account.")
    print(f"Phone number: {config.PHONE_NUMBER}")
    print()
    print("You will be prompted for:")
    print("  1. Verification code (sent to your Telegram app)")
    print("  2. 2FA password (if enabled)")
    print()
    print("=" * 70)
    print()
    
    # Create client
    client = TelegramClient(
        config.SESSION_NAME,
        config.API_ID,
        config.API_HASH
    )
    
    try:
        # Start client with phone number
        await client.start(phone=config.PHONE_NUMBER)
        
        # Get user info
        me = await client.get_me()
        
        print()
        print("=" * 70)
        print("✅ SESSION CREATED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print(f"Logged in as: {me.first_name} {me.last_name or ''}")
        print(f"Phone: {me.phone}")
        print(f"Username: @{me.username}" if me.username else "Username: None")
        print(f"Premium: {'Yes ✅' if me.premium else 'No ❌'}")
        print()
        
        if me.premium:
            print("✅ You have Telegram Premium - 4GB file support enabled!")
        else:
            print("⚠️  You don't have Telegram Premium - file limit is 2GB")
            print("   Upgrade to Premium for 4GB file support")
        
        print()
        print(f"Session file created: {config.SESSION_FILE}")
        print()
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Session file will be uploaded to Fly.io")
        print("  2. Userbot will start automatically")
        print("  3. Send .start to any chat to see commands")
        print()
        print("=" * 70)
        
        # Disconnect
        await client.disconnect()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR CREATING SESSION")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("Please try again or check your credentials.")
        print()
        print("=" * 70)
        
        return False


if __name__ == "__main__":
    success = asyncio.run(create_session())
    sys.exit(0 if success else 1)
