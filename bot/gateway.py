
from interactions import Interaction
from info import get, save
from dotenv import load_dotenv
import websockets
import asyncio
import os
import json

load_dotenv()


class Gateway:
    def __init__(self):
        self.token = os.getenv("TOKEN")
        self.message = asyncio.Queue()
        self.heartbeat = 1
        self.session_id = None 
        
    async def connect(self):
        info = get()
        gateway_url = info["gateway_url"]
        async with websockets.connect(gateway_url) as websocket:
            event = await websocket.recv()
            print(f'from connect {event}\n')
            event = json.loads(event)
            gateway_event_handler = asyncio.create_task(self.gateway_event_handler(event))
            send = asyncio.create_task(self.send(websocket))
            recv = asyncio.create_task(self.recv(websocket))
            await gateway_event_handler
            await send 
            await recv
            
    async def send(self, ws):
        while True:
            msg = json.dumps(await self.message.get())
            await ws.send(msg)

    async def recv(self, ws):
        while True:
            try:
                event = await ws.recv()
                print(f'from recv {event}\n')
                event = json.loads(event)
                gateway_event_handler = asyncio.create_task(self.gateway_event_handler(event))
                await gateway_event_handler
            except websockets.ConnectionClosed:
                resume_con = asyncio.create_task(self.resume(ws))
                await resume_con

    async def ping(self):
        while True:
            msg = {"op": 1, "d": self.heartbeat}
            await self.message.put(msg)
            await asyncio.sleep(self.heartbeat / 1000)

    async def resume(self, ws):
        await ws.close(code=1000)
        resume = {
            "op": 6,
            "d": {
                "token": self.token,
                "session_id": self.session_id,
                "seq": 0,
            }
        }
        # sequence number from last event recieved
        await self.message.put(resume)

    def run(self):
        data = {
            "gateway_url": "wss://gateway.discord.gg/",
            "lib_name": "discord_bot"
        }
        save(data)
        asyncio.run(self.connect())
    
    async def gateway_event_handler(self, event):
        event_name = event["t"]
        interaction = Interaction()

        if event["op"] == 10:
            info = get()

            lib_name = info["lib_name"]
            self.heartbeat = event["d"]["heartbeat_interval"]
            ping = asyncio.create_task(self.ping())
            
            identity = {
                "op": 2,
                "d": {
                    "token": self.token,
                    "intents": 1 << 0,
                    "properties": {
                        "$os": "linux",
                        "$browser": lib_name,
                        "$device": lib_name,
                    },
                }
            }
            await self.message.put(identity)
            await ping

        sequence = event["s"]
        if sequence:
            save({"sequence": sequence})
            
        if event_name == "GUILD_CREATE":
            guild_id = event["d"]["id"]
            data = {"guild_id": guild_id}
            save(data)

        if event_name == "READY":
            session_id = event["d"]["session_id"]
            resume_gateway_url = event['d']['resume_gateway_url']
            data = {"session_id": session_id, "resume_gateway_url": resume_gateway_url}
            save(data)
            interaction.create_message()

        if event_name == "INTERACTION_CREATE":
            interaction.response(event)


if __name__ == "__main__":
    gateway = Gateway()
    gateway.run()
    
