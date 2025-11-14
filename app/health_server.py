"""
Simple health check server for uptime monitoring
Runs alongside the Telethon userbot
"""
import asyncio
import logging
from aiohttp import web
from app import config

logger = logging.getLogger(__name__)


async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "userbot": "running",
        "type": "telethon"
    })


async def status_check(request):
    """Status endpoint"""
    return web.json_response({
        "userbot": "running",
        "session": "active",
        "type": "telethon_userbot",
        "features": {
            "4gb_support": True,
            "progress_bars": True,
            "ipa_patching": True
        }
    })


async def root(request):
    """Root endpoint"""
    return web.json_response({
        "bot": "IPA Patcher Userbot",
        "type": "telethon",
        "status": "online"
    })


async def start_health_server():
    """Start the health check server"""
    app = web.Application()
    app.router.add_get('/', root)
    app.router.add_get('/health', health_check)
    app.router.add_get('/status', status_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, config.HOST, config.HEALTH_PORT)
    await site.start()
    
    logger.info(f"✅ Health server started on {config.HOST}:{config.HEALTH_PORT}")
    
    # Keep running
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(start_health_server())
