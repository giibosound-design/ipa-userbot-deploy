"""
Telethon IPA Patcher Userbot
Runs as a user account with full 4GB file support
"""
import os
import time
import logging
from pathlib import Path
from telethon import TelegramClient, events
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
user_files = {}


@client.on(events.NewMessage(pattern=r'^\.start$', outgoing=True))
async def start_command(event):
    """Handle .start command"""
    await event.edit(
        "🤖 **IPA Patcher Userbot**\n\n"
        "**Commands:**\n"
        "`.patch` - Reply to an IPA file to patch it\n"
        "`.help` - Show this message\n"
        "`.status` - Show userbot status\n\n"
        "**Features:**\n"
        "🔧 Patch IPA with blatantsPatch.dylib\n"
        "📊 4GB file support (Telegram Premium)\n"
        "⚡ Fancy progress bars\n"
        "🚀 Fast upload/download speeds\n\n"
        "Upload an IPA file and reply with `.patch`"
    )


@client.on(events.NewMessage(pattern=r'^\.help$', outgoing=True))
async def help_command(event):
    """Handle .help command"""
    await event.edit(
        "📖 **Help & Commands**\n\n"
        "**Commands:**\n"
        "`.start` - Show welcome message\n"
        "`.help` - Show this help\n"
        "`.patch` - Patch IPA file (reply to file)\n"
        "`.status` - Show userbot status\n\n"
        "**How to use:**\n"
        "1️⃣ Upload an IPA file (up to 4GB)\n"
        "2️⃣ Reply to the file with `.patch`\n"
        "3️⃣ Wait for processing\n"
        "4️⃣ Download your patched IPA\n\n"
        "**Features:**\n"
        "• 4GB file support\n"
        "• Fast upload/download\n"
        "• Progress bars\n"
        "• Automatic cleanup\n"
    )


@client.on(events.NewMessage(pattern=r'^\.status$', outgoing=True))
async def status_command(event):
    """Handle .status command"""
    me = await client.get_me()
    
    status_text = (
        "📊 **Userbot Status**\n\n"
        f"**User:** {me.first_name}\n"
        f"**Phone:** {me.phone}\n"
        f"**Premium:** {'Yes ✅' if me.premium else 'No ❌'}\n\n"
        f"**Session:** Active ✅\n"
        f"**4GB Support:** {'Yes ✅' if me.premium else 'Limited to 2GB'}\n"
    )
    
    await event.edit(status_text)


@client.on(events.NewMessage(pattern=r'^\.patch$', outgoing=True))
async def patch_command(event):
    """Handle .patch command"""
    # Check if replying to a message
    if not event.is_reply:
        await event.edit("❌ Please reply to an IPA file with `.patch`")
        return
    
    # Get replied message
    replied_msg = await event.get_reply_message()
    
    # Check if message has a document
    if not replied_msg.document:
        await event.edit("❌ Please reply to an IPA file")
        return
    
    # Get file name
    file_name = None
    for attr in replied_msg.document.attributes:
        if isinstance(attr, DocumentAttributeFilename):
            file_name = attr.file_name
            break
    
    if not file_name:
        file_name = "unknown.ipa"
    
    # Check file extension
    if not file_name.lower().endswith('.ipa'):
        await event.edit("❌ File must be an IPA file (.ipa extension)")
        return
    
    # Start processing
    status_msg = await event.edit(
        f"📥 **Downloading {file_name}**\n\n"
        f"Size: {human_readable_size(replied_msg.document.size)}\n"
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
            replied_msg.document,
            file=file_path,
            progress_callback=progress
        )
        
        download_size = os.path.getsize(file_path)
        
        await status_msg.edit(
            f"✅ **Download complete!**\n\n"
            f"📱 File: {file_name}\n"
            f"📦 Size: {human_readable_size(download_size)}\n\n"
            "🔧 Starting patching process..."
        )
        
        # Patch IPA
        await status_msg.edit(
            "🔧 **Patching IPA**\n\n"
            "⏳ Processing...\n"
            f"Input: {file_name}\n"
            "Dylib: blatantsPatch.dylib\n\n"
            "This may take a few minutes..."
        )
        
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
                        f"📦 Size: {human_readable_size(patched_size)}",
                attributes=[DocumentAttributeFilename(Path(result).name)],
                progress_callback=progress
            )
            
            await status_msg.edit(
                "✅ **IPA Patched Successfully!**\n\n"
                f"📱 Output: {Path(result).name}\n"
                f"📦 Size: {human_readable_size(patched_size)}\n\n"
                "Your patched IPA has been sent!"
            )
            
            # Cleanup
            ipa_ops.cleanup_file(file_path)
            ipa_ops.cleanup_file(result)
            
        else:
            await status_msg.edit(
                f"❌ **Patching Failed**\n\n"
                f"Error: {result[:200]}\n\n"
                "Please try again or check your IPA file."
            )
            ipa_ops.cleanup_file(file_path)
            
    except Exception as e:
        logger.error(f"Error in patch_command: {e}")
        await status_msg.edit(
            f"❌ **Error during processing**\n\n"
            f"Error: {str(e)[:200]}\n\n"
            "Please try again."
        )


async def main():
    """Main function to start the userbot"""
    logger.info("🚀 Starting IPA Patcher Userbot...")
    
    # Start client
    await client.start(phone=config.PHONE_NUMBER)
    
    me = await client.get_me()
    logger.info(f"✅ Logged in as {me.first_name} ({me.phone})")
    logger.info(f"📊 Premium: {me.premium}")
    logger.info(f"🔧 4GB Support: {'Yes' if me.premium else 'No (upgrade to Premium)'}")
    
    logger.info("✅ Userbot is running!")
    logger.info("📝 Send .start to any chat to see commands")
    
    # Keep running
    await client.run_until_disconnected()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
