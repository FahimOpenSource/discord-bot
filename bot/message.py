
# from role import Select_role
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = "https://discord.com/api/v9"

class Message():
    def __init__(self):
        self.token = os.getenv("TOKEN")

    def create_message(self):
        # Before that check_msg()
        self.url = f"{API_URL}/channels/967526705088565248/messages"
        # Make the url get channel id from Guild create payload

        # Roles
        message = {
            "content": "Which platform do you play on?",
            "tts": False,
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "PC",
                            "style": 2,
                            "custom_id": "pc"
                        },
                        {
                            "type": 2,
                            "label": "Xbox",
                            "style": 2,
                            "custom_id": "xbox"
                        },
                        {
                            "type": 2,
                            "label": "PlayStation",
                            "style": 2,
                            "custom_id": "playstation",
                            
                        },
                        {
                            "type": 2,
                            "label": "Nintendo Switch",
                            "style": 2,
                            "custom_id": "switch",
                        },
                        
                        {
                            "type": 2,
                            "label": "Mobile",
                            "style": 2,
                            "custom_id": "mobile",
                        }
                    ]
                }
            ]
        }
        
        msg = json.dumps(message)
        headers = {"Authorization": f"Bot {self.token}", "Content-Type": "application/json"}
        res = requests.post(self.url,data=msg, headers=headers)
        res = json.loads(res.text)
        
        print(f'tttttttttttttt   {res}')


    def check_msg(self):

        pass
    
    # def send_reply(self,event):
    #     data = event["data"]
    #     user = event["member"]["user"]
    #     if data["component_type"] == 2:
    #         role = data["custom_id"]
    #         Select_role(role,user)

            # this means some one clicked on a botton to choose a role 
            #  select a role 
            # return 
            # then respond

    