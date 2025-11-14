"""
Main entry point for IPA Patcher Userbot
Runs both Telethon userbot and health check server
"""
import asyncio
import logging
from app.userbot import client, main as userbot_main
from app.health_server import start_health_server
from app import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)


async def main():
    """Run both userbot and health server"""
    logger.info("🚀 Starting IPA Patcher Userbot System...")
    
    # Start both tasks concurrently
    await asyncio.gather(
        userbot_main(),
        start_health_server()
    )


if __name__ == "__main__":
    asyncio.run(main())
