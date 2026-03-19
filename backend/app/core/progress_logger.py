import asyncio
from datetime import datetime

class ProgressEmitter:
    def __init__(self, send_func):
        self.send = send_func

    async def log(self, message: str, level: str = "info", progress=None):
        await self.send({
            "time": datetime.now().strftime("%H:%M:%S"),
            "level": level,
            "message": message,
            "progress": progress
        })

    def sync_log(self, message, level="info", progress=None):
        """Allow logging from threadpool / sync code."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.log(message, level, progress))
        except RuntimeError:
            asyncio.run(self.log(message, level, progress))
