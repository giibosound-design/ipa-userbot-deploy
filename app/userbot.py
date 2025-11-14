"""
Telethon IPA Patcher Userbot - Production Ready
Runs as a user account with full 4GB file support
"""
import os
import time
import logging
import asyncio
from pathlib import Path
from telethon import TelegramClient, events, Button
from telethon.tl.types import DocumentAttributeFilename
from app import config
from app.operations import IPAOperations
from app.progress import ProgressBar, human_readable_size

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

# Initialize Telethon client
client = TelegramClient(
    config.SESSION_NAME,
    config.API_ID,
    config.API_HASH
)

# Initialize IPA operations
ipa_ops = IPAOperations(
    temp_dir=config.TEMP_DIR,
    ipapatch_bin=config.IPAPATCH_BINARY,
    dylib_path=config.DYLIB_PATH
)

# User sessions
user_sessions = {}


def get_main_menu():
    """Get main menu keyboard"""
    return [
        [Button.inline("🔧 Patch IPA", b"patch_ipa")],
        [Button.inline("📊 Bot Status", b"bot_status")],
        [Button.inline("ℹ️ Help", b"show_help")],
        [Button.inline("🗑️ Clear Files", b"clear_files")]
    ]


@client.on(events.NewMessage(pattern=r'^/start$'))
async def start_command(event):
    """Handle /start command"""
    try:
        await event.respond(
            "🤖 **IPA Patcher Bot**\n\n"
            "Welcome! I can patch IPA files with blatantsPatch.dylib.\n\n"
            "**Features:**\n"
            "🔧 Automatic IPA patching\n"
            "📊 4GB file support (Premium)\n"
            "⚡ Fast upload/download speeds\n"
            "📈 Real-time progress bars\n\n"
            "**How to use:**\n"
            "1. Upload an IPA file\n"
            "2. Click 'Patch IPA' button\n"
            "3. Download your patched IPA!\n\n"
            "Choose an option below:",
            buttons=get_main_menu()
        )
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await event.respond("❌ Error showing menu. Please try /start again.")


@client.on(events.NewMessage(pattern=r'^/help$'))
async def help_command(event):
    """Handle /help command"""
    try:
        await event.respond(
            "📖 **Help & Commands**\n\n"
            "**Commands:**\n"
            "/start - Show main menu\n"
            "/help - Show this help\n"
            "/status - Show bot status\n"
            "/clear - Clear all uploaded files\n\n"
            "**How to patch IPA:**\n"
            "1️⃣ Upload an IPA file (up to 4GB)\n"
            "2️⃣ Click the 'Patch IPA' button\n"
            "3️⃣ Wait for processing\n"
            "4️⃣ Download your patched IPA\n\n"
            "**Supported files:**\n"
            "• .ipa - iOS applications\n"
            "• .deb - Debian packages\n"
            "• .dylib - Dynamic libraries\n\n"
            "**Features:**\n"
            "✅ 4GB file support\n"
            "✅ Fast upload/download\n"
            "✅ Progress bars\n"
            "✅ Automatic cleanup",
            buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
        )
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        await event.respond("❌ Error showing help. Please try /help again.")


@client.on(events.NewMessage(pattern=r'^/status$'))
async def status_command(event):
    """Handle /status command"""
    try:
        me = await client.get_me()
        
        # Count files in session
        chat_id = event.chat_id
        file_count = len(user_sessions.get(chat_id, {}).get('files', []))
        
        status_text = (
            "📊 **Bot Status**\n\n"
            f"**User:** {me.first_name}\n"
            f"**Username:** @{me.username}\n"
            f"**Premium:** {'Yes ✅' if me.premium else 'No ❌'}\n"
            f"**4GB Support:** {'Enabled ✅' if me.premium else 'Limited to 2GB'}\n\n"
            f"**Session:** Active ✅\n"
            f"**Files in queue:** {file_count}\n"
            f"**Bot:** Running ✅"
        )
        
        await event.respond(
            status_text,
            buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
        )
    except Exception as e:
        logger.error(f"Error in status_command: {e}")
        await event.respond("❌ Error getting status. Please try /status again.")


@client.on(events.NewMessage(pattern=r'^/clear$'))
async def clear_command(event):
    """Handle /clear command"""
    try:
        chat_id = event.chat_id
        
        # Clear user session
        if chat_id in user_sessions:
            files = user_sessions[chat_id].get('files', [])
            for file_path in files:
                try:
                    ipa_ops.cleanup_file(file_path)
                except:
                    pass
            user_sessions[chat_id] = {'files': []}
        
        await event.respond(
            "🗑️ **Files Cleared**\n\n"
            "All uploaded files have been removed.",
            buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
        )
    except Exception as e:
        logger.error(f"Error in clear_command: {e}")
        await event.respond("❌ Error clearing files. Please try /clear again.")


@client.on(events.CallbackQuery(pattern=b"main_menu"))
async def main_menu_callback(event):
    """Show main menu"""
    try:
        await event.edit(
            "🤖 **IPA Patcher Bot**\n\n"
            "Choose an option below:",
            buttons=get_main_menu()
        )
    except Exception as e:
        logger.error(f"Error in main_menu_callback: {e}")


@client.on(events.CallbackQuery(pattern=b"show_help"))
async def help_callback(event):
    """Show help"""
    try:
        await event.edit(
            "📖 **Help & Commands**\n\n"
            "**Commands:**\n"
            "/start - Show main menu\n"
            "/help - Show this help\n"
            "/status - Show bot status\n"
            "/clear - Clear all uploaded files\n\n"
            "**How to patch IPA:**\n"
            "1️⃣ Upload an IPA file (up to 4GB)\n"
            "2️⃣ Click the 'Patch IPA' button\n"
            "3️⃣ Wait for processing\n"
            "4️⃣ Download your patched IPA\n\n"
            "**Supported files:**\n"
            "• .ipa - iOS applications\n"
            "• .deb - Debian packages\n"
            "• .dylib - Dynamic libraries",
            buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
        )
    except Exception as e:
        logger.error(f"Error in help_callback: {e}")


@client.on(events.CallbackQuery(pattern=b"bot_status"))
async def status_callback(event):
    """Show bot status"""
    try:
        me = await client.get_me()
        chat_id = event.chat_id
        file_count = len(user_sessions.get(chat_id, {}).get('files', []))
        
        await event.edit(
            "📊 **Bot Status**\n\n"
            f"**User:** {me.first_name}\n"
            f"**Username:** @{me.username}\n"
            f"**Premium:** {'Yes ✅' if me.premium else 'No ❌'}\n"
            f"**4GB Support:** {'Enabled ✅' if me.premium else 'Limited to 2GB'}\n\n"
            f"**Session:** Active ✅\n"
            f"**Files in queue:** {file_count}\n"
            f"**Bot:** Running ✅",
            buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
        )
    except Exception as e:
        logger.error(f"Error in status_callback: {e}")


@client.on(events.CallbackQuery(pattern=b"clear_files"))
async def clear_callback(event):
    """Clear files"""
    try:
        chat_id = event.chat_id
        
        if chat_id in user_sessions:
            files = user_sessions[chat_id].get('files', [])
            for file_path in files:
                try:
                    ipa_ops.cleanup_file(file_path)
                except:
                    pass
            user_sessions[chat_id] = {'files': []}
        
        await event.edit(
            "🗑️ **Files Cleared**\n\n"
            "All uploaded files have been removed.",
            buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
        )
    except Exception as e:
        logger.error(f"Error in clear_callback: {e}")


@client.on(events.CallbackQuery(pattern=b"patch_ipa"))
async def patch_callback(event):
    """Handle patch IPA button"""
    try:
        chat_id = event.chat_id
        
        # Check if user has uploaded files
        if chat_id not in user_sessions or not user_sessions[chat_id].get('files'):
            await event.answer("⚠️ Please upload an IPA file first!", alert=True)
            return
        
        # Get the last uploaded file
        last_file = user_sessions[chat_id]['files'][-1]
        
        if not last_file.endswith('.ipa'):
            await event.answer("⚠️ Please upload an IPA file!", alert=True)
            return
        
        await event.answer("🔧 Starting patch process...")
        
        # Start patching
        await patch_ipa_file(event, last_file)
        
    except Exception as e:
        logger.error(f"Error in patch_callback: {e}")
        await event.answer("❌ Error starting patch. Please try again.", alert=True)


async def patch_ipa_file(event, file_path):
    """Patch IPA file"""
    try:
        file_name = Path(file_path).name
        
        # Send processing message
        status_msg = await event.respond(
            f"🔧 **Patching IPA**\n\n"
            f"📱 File: {file_name}\n"
            f"📦 Size: {human_readable_size(os.path.getsize(file_path))}\n\n"
            "⏳ Processing...\n"
            "This may take a few minutes...",
            buttons=None
        )
        
        # Patch IPA
        success, result = ipa_ops.patch_ipa(file_path)
        
        if success:
            patched_size = os.path.getsize(result)
            
            # Upload patched IPA
            await status_msg.edit(
                "📤 **Uploading patched IPA...**\n\n"
                "Please wait..."
            )
            
            progress = ProgressBar(status_msg, "📤 Uploading...")
            
            await client.send_file(
                event.chat_id,
                result,
                caption=f"✅ **Patched IPA Ready!**\n\n"
                        f"📱 File: {Path(result).name}\n"
                        f"📦 Size: {human_readable_size(patched_size)}\n\n"
                        f"Patched with blatantsPatch.dylib",
                attributes=[DocumentAttributeFilename(Path(result).name)],
                progress_callback=progress,
                buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
            )
            
            await status_msg.edit(
                "✅ **IPA Patched Successfully!**\n\n"
                f"📱 Output: {Path(result).name}\n"
                f"📦 Size: {human_readable_size(patched_size)}\n\n"
                "Your patched IPA has been sent!",
                buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
            )
            
            # Cleanup
            ipa_ops.cleanup_file(file_path)
            ipa_ops.cleanup_file(result)
            
        else:
            await status_msg.edit(
                f"❌ **Patching Failed**\n\n"
                f"Error: {result[:200]}\n\n"
                "Please try again with a different IPA file.",
                buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
            )
            ipa_ops.cleanup_file(file_path)
            
    except Exception as e:
        logger.error(f"Error in patch_ipa_file: {e}")
        try:
            await event.respond(
                f"❌ **Error during processing**\n\n"
                f"An unexpected error occurred.\n\n"
                "Please try again or contact support.",
                buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
            )
        except:
            pass


@client.on(events.NewMessage)
async def handle_file_upload(event):
    """Handle file uploads"""
    try:
        # Ignore commands
        if event.message.text and event.message.text.startswith('/'):
            return
        
        # Check if message has a document
        if not event.message.document:
            return
        
        # Get file name
        file_name = None
        for attr in event.message.document.attributes:
            if isinstance(attr, DocumentAttributeFilename):
                file_name = attr.file_name
                break
        
        if not file_name:
            return
        
        # Check file extension
        if not file_name.lower().endswith(('.ipa', '.deb', '.dylib')):
            return
        
        # Send upload confirmation
        status_msg = await event.respond(
            f"📥 **Downloading {file_name}**\n\n"
            f"Size: {human_readable_size(event.message.document.size)}\n"
            "Please wait..."
        )
        
        try:
            os.makedirs(config.TEMP_DIR, exist_ok=True)
            
            # Download file with progress
            file_path = os.path.join(
                config.TEMP_DIR,
                f"{int(time.time())}_{file_name}"
            )
            
            progress = ProgressBar(status_msg, "📥 Downloading...")
            
            await client.download_media(
                event.message.document,
                file=file_path,
                progress_callback=progress
            )
            
            download_size = os.path.getsize(file_path)
            
            # Store in user session
            chat_id = event.chat_id
            if chat_id not in user_sessions:
                user_sessions[chat_id] = {'files': []}
            user_sessions[chat_id]['files'].append(file_path)
            
            await status_msg.edit(
                f"✅ **Download complete!**\n\n"
                f"📱 File: {file_name}\n"
                f"📦 Size: {human_readable_size(download_size)}\n\n"
                "Click 'Patch IPA' to start patching:",
                buttons=[[Button.inline("🔧 Patch IPA", b"patch_ipa")],
                        [Button.inline("« Back to Menu", b"main_menu")]]
            )
            
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            await status_msg.edit(
                f"❌ **Download failed**\n\n"
                f"Error: {str(e)[:200]}\n\n"
                "Please try uploading again.",
                buttons=[[Button.inline("« Back to Menu", b"main_menu")]]
            )
            
    except Exception as e:
        logger.error(f"Error in handle_file_upload: {e}")


async def main():
    """Main function to start the userbot"""
    try:
        logger.info("🚀 Starting IPA Patcher Userbot...")
        
        # Start client
        await client.start(phone=config.PHONE_NUMBER)
        
        me = await client.get_me()
        logger.info(f"✅ Logged in as {me.first_name} (@{me.username})")
        logger.info(f"📊 Premium: {me.premium}")
        logger.info(f"🔧 4GB Support: {'Yes' if me.premium else 'No (upgrade to Premium)'}")
        
        logger.info("✅ Userbot is running!")
        logger.info("📝 Send /start to any chat to see the menu")
        
        # Keep running
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        # Wait and retry
        await asyncio.sleep(5)
        await main()


if __name__ == "__main__":
    asyncio.run(main())
