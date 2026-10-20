from httpx import AsyncClient
import os
import telebot.types
from bot_instance import bot
import asyncio

class Api:

    def __init__(self):

        self.client : AsyncClient = AsyncClient(timeout=10, base_url=os.getenv("API_URL"))

    async def new_answers(self, work_id, file : telebot.types.Document):

        file_info = await asyncio.to_thread(bot.get_file, file.file_id)
        file_bytes = await asyncio.to_thread(bot.download_file, file_info.file_path)

        async with self.client as c:

            r = await c.post(
                "answers",
                data={
                    "work_id": work_id
                },
                files={"file": (file.file_name, file_bytes, "application/pdf")}
            )

            if r.status_code != 201:

                raise Exception(f"Failed to publosh answer: {r.text}")

    async def get_answers(self, work_id):
            
        async with self.client as c:

            r = await c.get(f"answers?work_id={work_id}")

            if r.status_code != 201:

                raise Exception(f"Failed to publosh answer: {r.text}")

            return r.text
    