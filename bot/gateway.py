
from message import Message
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
            res = await websocket.recv()
            print(f"Received: {res}")
            gateway_event_handler = asyncio.create_task(self.gateway_event_handler(res))
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
                res = json.loads(await ws.recv())
                print(f"Responce: {res}")
                gateway_event_handler = asyncio.create_task(self.gateway_event_handler(res))
                await self()
            except websockets.ConnectionClosedOK:
                resume_con = asyncio.create_task(self.resume(ws))
                await resume_con

    async def ping(self):
        while True:
            msg = {"op": 1, "d": self.heartbeat}
            await self.message.put(msg)
            await asyncio.sleep(self.heartbeat / 1000)

    # async def resume(self, ws):
    #     ws.close(code=1000)
    #     resume = {
    #         "op": 6,
    #         "d": {
    #             "token": self.token,
    #             "session_id": self.session_id,
    #             "seq": 0,
    #         }
    #     }
    #     #sequence number from last event recieved
    #     await self.message.put(resume)

    async def run(self):
        data = {
            "gateway_url": "wss://gateway.discord.gg/",
            "lib_name": "discord_bot"
        }
        save(data)
        asyncio.run(self.connect())
    
    async def gateway_event_handler(self, res):
        event = res["t"]
        msg = Message()

        if res["op"] == 10:
            info = get()

            lib_name = info["lib_name"]
            self.heartbeat = res["d"]["heartbeat_interval"]
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

        sequence_no = res["s"]
        if sequence_no is not None:
            info = get()
            if info["sequence"]:
                if sequence_no > info["sequence"]:
                    info["sequence"] = sequence_no
                    save(info)
            else:
                info["sequence"] = sequence_no
                save(info)
                # TODO: then maye be resume con.
            
        if event == "GUILD_CREATE":
            guild_id = res["d"]["id"]
            info = get()
            info["guild_id"] = guild_id
            save(info)

        if event == "READY":
            session_id = res["d"]["session_id"]
            info["session_id"] = session_id
            save(info)
            msg.create_message()

        if event == "INTERACTION_CREATE":
            msg.send_reply(self.res)



if __name__ == "__main__":
    gateway = Gateway()
    gateway.run()
    