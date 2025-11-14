"""
Telethon IPA Patcher Userbot - Single Window UI System
Professional, clean, single-message interface
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
from app.window_manager import (
    get_or_create_window, update_window, delete_window,
    get_user_state, set_user_state, clear_user_state,
    add_user_file, get_all_user_files, clear_user_files,
    clear_all_messages, reset_user
)
from app import ui_style as ui

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


def get_main_menu_buttons():
    """Get main menu keyboard"""
    return [
        [Button.inline(f"{ui.EMOJI['patch']} Patch IPA", b"patch_ipa")],
        [
            Button.inline(f"{ui.EMOJI['status']} Status", b"show_status"),
            Button.inline(f"{ui.EMOJI['help']} Help", b"show_help")
        ],
        [
            Button.inline(f"{ui.EMOJI['settings']} Settings", b"show_settings"),
            Button.inline(f"{ui.EMOJI['about']} About", b"show_about")
        ],
        [Button.inline(f"{ui.EMOJI['clear']} Clear All", b"confirm_clear")]
    ]


def get_back_button():
    """Get back to menu button"""
    return [[Button.inline(f"{ui.EMOJI['back']} Back to Menu", b"main_menu")]]


async def show_main_menu(event):
    """Show main menu in single window"""
    chat_id = event.chat_id
    
    # Get or create main window
    try:
        window = await get_or_create_window(
            client,
            event,
            ui.MAIN_MENU,
            get_main_menu_buttons()
        )
    except:
        # Fallback: send new message
        window = await event.respond(
            ui.MAIN_MENU,
            buttons=get_main_menu_buttons()
        )
    
    # Delete the command message if it's not the window
    try:
        if hasattr(event, 'message') and event.message.id != window.id:
            await event.message.delete()
    except:
        pass


# ============================================================================
# COMMAND HANDLERS
# ============================================================================

@client.on(events.NewMessage(pattern=r'^/start$'))
async def cmd_start(event):
    """Handle /start command"""
    try:
        await show_main_menu(event)
    except Exception as e:
        logger.error(f"Error in /start: {e}")


@client.on(events.NewMessage(pattern=r'^/menu$'))
async def cmd_menu(event):
    """Handle /menu command"""
    try:
        await show_main_menu(event)
    except Exception as e:
        logger.error(f"Error in /menu: {e}")


@client.on(events.NewMessage(pattern=r'^/help$'))
async def cmd_help(event):
    """Handle /help command"""
    try:
        chat_id = event.chat_id
        
        # Update window or create new one
        success = await update_window(
            client,
            chat_id,
            ui.HELP_TEXT,
            get_back_button()
        )
        
        if not success:
            await show_main_menu(event)
        
        # Delete command message
        try:
            await event.message.delete()
        except:
            pass
            
    except Exception as e:
        logger.error(f"Error in /help: {e}")


@client.on(events.NewMessage(pattern=r'^/status$'))
async def cmd_status(event):
    """Handle /status command"""
    try:
        chat_id = event.chat_id
        me = await client.get_me()
        
        user_info = {
            'name': f"{me.first_name} {me.last_name or ''}".strip(),
            'username': me.username or 'none',
            'premium': me.premium
        }
        
        file_count = len(get_all_user_files(chat_id))
        
        # Update window
        success = await update_window(
            client,
            chat_id,
            ui.status_text(user_info, file_count),
            get_back_button()
        )
        
        if not success:
            await show_main_menu(event)
        
        # Delete command message
        try:
            await event.message.delete()
        except:
            pass
            
    except Exception as e:
        logger.error(f"Error in /status: {e}")


@client.on(events.NewMessage(pattern=r'^/clear$'))
async def cmd_clear(event):
    """Handle /clear command - show confirmation"""
    try:
        chat_id = event.chat_id
        
        # Show confirmation
        success = await update_window(
            client,
            chat_id,
            ui.CLEAR_CONFIRM_TEXT,
            [
                [Button.inline(f"{ui.EMOJI['error']} Yes, Clear All", b"do_clear")],
                [Button.inline(f"{ui.EMOJI['back']} Cancel", b"main_menu")]
            ]
        )
        
        if not success:
            await show_main_menu(event)
        
        # Delete command message
        try:
            await event.message.delete()
        except:
            pass
            
    except Exception as e:
        logger.error(f"Error in /clear: {e}")


# ============================================================================
# CALLBACK HANDLERS
# ============================================================================

@client.on(events.CallbackQuery(pattern=b"main_menu"))
async def cb_main_menu(event):
    """Show main menu"""
    try:
        chat_id = event.chat_id
        
        await update_window(
            client,
            chat_id,
            ui.MAIN_MENU,
            get_main_menu_buttons()
        )
        
        await event.answer()
    except Exception as e:
        logger.error(f"Error in main_menu callback: {e}")
        await event.answer(f"{ui.EMOJI['error']} Error", alert=True)


@client.on(events.CallbackQuery(pattern=b"show_help"))
async def cb_help(event):
    """Show help"""
    try:
        chat_id = event.chat_id
        
        await update_window(
            client,
            chat_id,
            ui.HELP_TEXT,
            get_back_button()
        )
        
        await event.answer()
    except Exception as e:
        logger.error(f"Error in help callback: {e}")
        await event.answer(f"{ui.EMOJI['error']} Error", alert=True)


@client.on(events.CallbackQuery(pattern=b"show_status"))
async def cb_status(event):
    """Show status"""
    try:
        chat_id = event.chat_id
        me = await client.get_me()
        
        user_info = {
            'name': f"{me.first_name} {me.last_name or ''}".strip(),
            'username': me.username or 'none',
            'premium': me.premium
        }
        
        file_count = len(get_all_user_files(chat_id))
        
        await update_window(
            client,
            chat_id,
            ui.status_text(user_info, file_count),
            get_back_button()
        )
        
        await event.answer()
    except Exception as e:
        logger.error(f"Error in status callback: {e}")
        await event.answer(f"{ui.EMOJI['error']} Error", alert=True)


@client.on(events.CallbackQuery(pattern=b"show_settings"))
async def cb_settings(event):
    """Show settings"""
    try:
        chat_id = event.chat_id
        
        await update_window(
            client,
            chat_id,
            ui.SETTINGS_TEXT,
            get_back_button()
        )
        
        await event.answer()
    except Exception as e:
        logger.error(f"Error in settings callback: {e}")
        await event.answer(f"{ui.EMOJI['error']} Error", alert=True)


@client.on(events.CallbackQuery(pattern=b"show_about"))
async def cb_about(event):
    """Show about"""
    try:
        chat_id = event.chat_id
        
        await update_window(
            client,
            chat_id,
            ui.ABOUT_TEXT,
            get_back_button()
        )
        
        await event.answer()
    except Exception as e:
        logger.error(f"Error in about callback: {e}")
        await event.answer(f"{ui.EMOJI['error']} Error", alert=True)


@client.on(events.CallbackQuery(pattern=b"confirm_clear"))
async def cb_confirm_clear(event):
    """Show clear confirmation"""
    try:
        chat_id = event.chat_id
        
        await update_window(
            client,
            chat_id,
            ui.CLEAR_CONFIRM_TEXT,
            [
                [Button.inline(f"{ui.EMOJI['error']} Yes, Clear All", b"do_clear")],
                [Button.inline(f"{ui.EMOJI['back']} Cancel", b"main_menu")]
            ]
        )
        
        await event.answer()
    except Exception as e:
        logger.error(f"Error in confirm_clear callback: {e}")
        await event.answer(f"{ui.EMOJI['error']} Error", alert=True)


@client.on(events.CallbackQuery(pattern=b"do_clear"))
async def cb_do_clear(event):
    """Execute clear all"""
    try:
        chat_id = event.chat_id
        
        await event.answer(f"{ui.EMOJI['processing']} Clearing...")
        
        # Clean up files
        files = get_all_user_files(chat_id)
        for file_path in files:
            try:
                ipa_ops.cleanup_file(file_path)
            except:
                pass
        
        # Reset user
        await reset_user(client, chat_id)
        
        # Show fresh start
        await client.send_message(
            chat_id,
            ui.CLEARED_TEXT + "\n\n" + ui.MAIN_MENU,
            buttons=get_main_menu_buttons()
        )
        
    except Exception as e:
        logger.error(f"Error in do_clear callback: {e}")
        await event.answer(f"{ui.EMOJI['error']} Error clearing", alert=True)


@client.on(events.CallbackQuery(pattern=b"patch_ipa"))
async def cb_patch_ipa(event):
    """Handle patch IPA button"""
    try:
        chat_id = event.chat_id
        
        # Check if user has uploaded files
        files = get_all_user_files(chat_id)
        if not files:
            await event.answer(f"{ui.EMOJI['warning']} Please upload an IPA file first!", alert=True)
            return
        
        # Get the last uploaded file
        last_file = files[-1]
        
        if not last_file.endswith('.ipa'):
            await event.answer(f"{ui.EMOJI['warning']} Please upload an IPA file!", alert=True)
            return
        
        await event.answer(f"{ui.EMOJI['processing']} Starting patch process...")
        
        # Start patching
        await patch_ipa_file(event, last_file)
        
    except Exception as e:
        logger.error(f"Error in patch_ipa callback: {e}")
        await event.answer(f"{ui.EMOJI['error']} Error starting patch", alert=True)


# ============================================================================
# FILE HANDLING
# ============================================================================

async def patch_ipa_file(event, file_path):
    """Patch IPA file with progress updates"""
    try:
        chat_id = event.chat_id
        file_name = Path(file_path).name
        file_size = human_readable_size(os.path.getsize(file_path))
        
        # Show patching progress
        await update_window(
            client,
            chat_id,
            ui.patching_progress_text(file_name, file_size),
            None
        )
        
        # Patch IPA
        success, result = ipa_ops.patch_ipa(file_path)
        
        if success:
            patched_size = human_readable_size(os.path.getsize(result))
            patched_name = Path(result).name
            
            # Upload patched IPA (outside the main window)
            await client.send_file(
                chat_id,
                result,
                caption=ui.success_text(patched_name, patched_size),
                attributes=[DocumentAttributeFilename(patched_name)]
            )
            
            # Update main window to show success
            await update_window(
                client,
                chat_id,
                ui.success_text(patched_name, patched_size),
                get_back_button()
            )
            
            # Cleanup
            ipa_ops.cleanup_file(file_path)
            ipa_ops.cleanup_file(result)
            clear_user_files(chat_id)
            
        else:
            # Show error
            await update_window(
                client,
                chat_id,
                ui.error_text(result),
                get_back_button()
            )
            ipa_ops.cleanup_file(file_path)
            clear_user_files(chat_id)
            
    except Exception as e:
        logger.error(f"Error in patch_ipa_file: {e}")
        try:
            await update_window(
                client,
                event.chat_id,
                ui.error_text(str(e)),
                get_back_button()
            )
        except:
            pass


@client.on(events.NewMessage)
async def handle_file_upload(event):
    """Handle file uploads and forwarded files"""
    try:
        # Ignore if it's a command
        if event.message.text and event.message.text.startswith('/'):
            return
        
        # Check if message has a document
        if not event.message.document:
            # Delete non-file, non-command messages
            try:
                await event.message.delete()
            except:
                pass
            return
        
        # Get file name
        file_name = None
        for attr in event.message.document.attributes:
            if isinstance(attr, DocumentAttributeFilename):
                file_name = attr.file_name
                break
        
        if not file_name:
            try:
                await event.message.delete()
            except:
                pass
            return
        
        # Check file extension
        if not file_name.lower().endswith(('.ipa', '.deb', '.dylib')):
            try:
                await event.message.delete()
            except:
                pass
            return
        
        chat_id = event.chat_id
        file_size = human_readable_size(event.message.document.size)
        
        # Check if file was forwarded
        is_forwarded = event.message.forward is not None
        
        # Show download progress in main window
        await update_window(
            client,
            chat_id,
            ui.download_progress_text(file_name, file_size, 0),
            None
        )
        
        try:
            os.makedirs(config.TEMP_DIR, exist_ok=True)
            
            # Download file
            file_path = os.path.join(
                config.TEMP_DIR,
                f"{int(time.time())}_{file_name}"
            )
            
            # Custom progress callback that updates main window
            async def progress_callback(current, total):
                percent = int((current / total) * 100)
                if percent % 10 == 0:  # Update every 10%
                    await update_window(
                        client,
                        chat_id,
                        ui.download_progress_text(file_name, file_size, percent),
                        None
                    )
            
            await client.download_media(
                event.message.document,
                file=file_path,
                progress_callback=progress_callback
            )
            
            # Store in user session
            add_user_file(chat_id, file_path)
            
            # Show file received
            await update_window(
                client,
                chat_id,
                ui.file_received_text(file_name, file_size, is_forwarded),
                [[Button.inline(f"{ui.EMOJI['patch']} Patch IPA", b"patch_ipa")],
                 [Button.inline(f"{ui.EMOJI['back']} Back to Menu", b"main_menu")]]
            )
            
            # Delete the uploaded/forwarded message
            try:
                await event.message.delete()
            except:
                pass
            
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            await update_window(
                client,
                chat_id,
                ui.error_text(f"Download failed: {str(e)}"),
                get_back_button()
            )
            
    except Exception as e:
        logger.error(f"Error in handle_file_upload: {e}")


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Main function to start the userbot"""
    try:
        logger.info(f"{ui.EMOJI['robot']} Starting IPA Patcher Userbot...")
        
        # Start client
        await client.start(phone=config.PHONE_NUMBER)
        
        me = await client.get_me()
        logger.info(f"{ui.EMOJI['success']} Logged in as {me.first_name} (@{me.username})")
        logger.info(f"{ui.EMOJI['status']} Premium: {me.premium}")
        logger.info(f"{ui.EMOJI['patch']} 4GB Support: {'Yes' if me.premium else 'No'}")
        
        logger.info(f"{ui.EMOJI['success']} Userbot is running!")
        logger.info(f"{ui.EMOJI['help']} Send /start to any chat to begin")
        
        # Keep running
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        # Wait and retry
        await asyncio.sleep(5)
        await main()


if __name__ == "__main__":
    asyncio.run(main())
