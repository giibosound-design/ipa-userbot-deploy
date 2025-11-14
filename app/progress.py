"""
Progress bar utilities for Telethon file operations
"""
import math
import time


def human_readable_size(size):
    """Convert bytes to human-readable format"""
    if size is None or size == 0:
        return "0B"
    power = 2**10
    n = 0
    units = ["B", "KB", "MB", "GB", "TB"]
    while size > power and n < 4:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


class ProgressBar:
    """Progress bar for Telethon upload/download operations"""
    
    def __init__(self, message, action="Processing"):
        self.message = message
        self.action = action
        self.start_time = time.time()
        self.last_update = 0
        
    async def __call__(self, current, total):
        """Progress callback for Telethon"""
        now = time.time()
        
        # Rate limit updates to once per second
        if now - self.last_update < 1:
            return
        
        self.last_update = now
        diff = now - self.start_time
        
        if diff == 0:
            diff = 1
        
        percentage = current * 100 / total
        speed = current / diff
        eta = round((total - current) / speed) if speed > 0 else 0
        
        bar_length = 25
        filled = math.floor(bar_length * percentage / 100)
        unfilled = bar_length - filled
        
        bar = "🟩" * filled + "⬜" * unfilled
        
        spinner = ["⏳", "⌛", "🔄", "🔃", "🔁"]
        anim = spinner[int(time.time()) % len(spinner)]
        
        progress_text = f"""
{self.action} {anim}

{bar}
**{percentage:.2f}%**

**Transferred:** {human_readable_size(current)} / {human_readable_size(total)}
**Speed:** {human_readable_size(speed)}/s
**ETA:** {eta} sec
""".strip()
        
        try:
            await self.message.edit(progress_text)
        except Exception:
            # Ignore edit errors
            pass
