from datetime import datetime

class ProgressEmitter:
    def __init__(self, send_func):
        self.send = send_func

    async def log(self, message: str, level: str = "info"):
        await self.send({
            "time": datetime.now().strftime("%H:%M:%S"),
            "level": level,
            "message": message
        })
