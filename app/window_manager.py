"""
Window Manager - Single Window UI System
Manages one main message per user that gets updated instead of sending new messages
"""
import logging
from typing import Dict, Optional, Any
from telethon import Button
from telethon.tl.types import Message

logger = logging.getLogger(__name__)

# Storage for main messages and user states
main_messages: Dict[int, Message] = {}
user_states: Dict[int, Dict[str, Any]] = {}


async def get_or_create_window(client, event, initial_text: str, initial_buttons=None) -> Message:
    """
    Get existing main window or create a new one
    
    Args:
        client: Telethon client
        event: Event object
        initial_text: Text to show if creating new window
        initial_buttons: Buttons to show if creating new window
    
    Returns:
        Message object of the main window
    """
    chat_id = event.chat_id
    
    # Check if main window exists
    if chat_id in main_messages:
        try:
            # Verify message still exists
            msg = main_messages[chat_id]
            await msg.get_reply_message()  # Test if message exists
            return msg
        except:
            # Message was deleted, remove from storage
            del main_messages[chat_id]
    
    # Create new main window
    try:
        msg = await client.send_message(
            chat_id,
            initial_text,
            buttons=initial_buttons
        )
        main_messages[chat_id] = msg
        logger.info(f"Created new main window for chat {chat_id}")
        return msg
    except Exception as e:
        logger.error(f"Error creating window: {e}")
        raise


async def update_window(client, chat_id: int, text: str, buttons=None, parse_mode='md') -> bool:
    """
    Update the main window with new content
    
    Args:
        client: Telethon client
        chat_id: Chat ID
        text: New text content
        buttons: New buttons (optional)
        parse_mode: Parse mode for text
    
    Returns:
        True if successful, False otherwise
    """
    if chat_id not in main_messages:
        logger.warning(f"No main window found for chat {chat_id}")
        return False
    
    try:
        msg = main_messages[chat_id]
        await msg.edit(
            text,
            buttons=buttons,
            parse_mode=parse_mode
        )
        logger.debug(f"Updated window for chat {chat_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating window for chat {chat_id}: {e}")
        # Try to recreate window
        try:
            del main_messages[chat_id]
        except:
            pass
        return False


async def delete_window(client, chat_id: int) -> bool:
    """
    Delete the main window
    
    Args:
        client: Telethon client
        chat_id: Chat ID
    
    Returns:
        True if successful, False otherwise
    """
    if chat_id not in main_messages:
        return False
    
    try:
        msg = main_messages[chat_id]
        await msg.delete()
        del main_messages[chat_id]
        logger.info(f"Deleted window for chat {chat_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting window for chat {chat_id}: {e}")
        # Remove from storage anyway
        try:
            del main_messages[chat_id]
        except:
            pass
        return False


def get_user_state(chat_id: int, key: str, default=None) -> Any:
    """
    Get user state value
    
    Args:
        chat_id: Chat ID
        key: State key
        default: Default value if not found
    
    Returns:
        State value or default
    """
    if chat_id not in user_states:
        user_states[chat_id] = {}
    
    return user_states[chat_id].get(key, default)


def set_user_state(chat_id: int, key: str, value: Any):
    """
    Set user state value
    
    Args:
        chat_id: Chat ID
        key: State key
        value: Value to set
    """
    if chat_id not in user_states:
        user_states[chat_id] = {}
    
    user_states[chat_id][key] = value
    logger.debug(f"Set state for chat {chat_id}: {key} = {value}")


def clear_user_state(chat_id: int):
    """
    Clear all state for a user
    
    Args:
        chat_id: Chat ID
    """
    if chat_id in user_states:
        del user_states[chat_id]
        logger.info(f"Cleared state for chat {chat_id}")


def get_all_user_files(chat_id: int) -> list:
    """
    Get all uploaded files for a user
    
    Args:
        chat_id: Chat ID
    
    Returns:
        List of file paths
    """
    return get_user_state(chat_id, 'files', [])


def add_user_file(chat_id: int, file_path: str):
    """
    Add a file to user's file list
    
    Args:
        chat_id: Chat ID
        file_path: Path to file
    """
    files = get_all_user_files(chat_id)
    files.append(file_path)
    set_user_state(chat_id, 'files', files)


def clear_user_files(chat_id: int):
    """
    Clear all files for a user
    
    Args:
        chat_id: Chat ID
    """
    set_user_state(chat_id, 'files', [])


async def clear_all_messages(client, chat_id: int, keep_last: int = 0):
    """
    Delete all messages in a chat
    
    Args:
        client: Telethon client
        chat_id: Chat ID
        keep_last: Number of recent messages to keep
    """
    try:
        # Get all messages
        messages = []
        async for message in client.iter_messages(chat_id, limit=100):
            messages.append(message.id)
        
        # Keep last N messages
        if keep_last > 0:
            messages = messages[keep_last:]
        
        # Delete messages
        if messages:
            await client.delete_messages(chat_id, messages)
            logger.info(f"Deleted {len(messages)} messages from chat {chat_id}")
        
        # Clear window reference
        if chat_id in main_messages:
            del main_messages[chat_id]
        
        return True
    except Exception as e:
        logger.error(f"Error clearing messages for chat {chat_id}: {e}")
        return False


async def reset_user(client, chat_id: int):
    """
    Complete reset for a user - clear all messages and state
    
    Args:
        client: Telethon client
        chat_id: Chat ID
    """
    try:
        # Clear all messages
        await clear_all_messages(client, chat_id)
        
        # Clear state
        clear_user_state(chat_id)
        
        # Clear window reference
        if chat_id in main_messages:
            del main_messages[chat_id]
        
        logger.info(f"Complete reset for chat {chat_id}")
        return True
    except Exception as e:
        logger.error(f"Error resetting user {chat_id}: {e}")
        return False
