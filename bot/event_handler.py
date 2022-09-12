
# from info import get, save
# from messages import Message
# from gateway import Gateway
# import asyncio

# class Gateway_Event_Handler(Gateway):
#     def __init__(self):
#         self.msg = Message()
#         self.event = self.res["t"]

#     async def identify(self,res):

        

#     def ready(self):
#         res = self.res

#         if self.event == "READY":
#             session_id = res["d"]["session_id"]
#             save({"session_id": session_id})
#             self.msg.create_message()

#     def interaction_create(self):
#         if self.event == "INTERACTION_CREATE":
#             self.msg.send_reply(self.res)

#             # handle interactions event
#             # run the msg.reply.
#             # store the id of the msg in txt file
            
