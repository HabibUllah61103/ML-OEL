import pickle
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio


class FrameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("frame_group", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("frame_group", self.channel_name)
        await self.send(text_data=json.dumps({"message": "Disconnected"}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        if message == "start":
            await self.start_streaming()

    async def start_streaming(self):
        filename = "Linear Regression.pkl"
        with open(filename, "rb") as file:
            loaded_model = pickle.load(file)
        asyncio.create_task()

    async def frame_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
