from role import Role
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = "https://discord.com/api/v9"


class Interaction:
    def __init__(self):
        self.token = os.getenv("TOKEN")
        self.headers = {"Authorization": f"Bot {self.token}", "Content-Type": "application/json"}

    def create_message(self):
        # Before that check_msg()
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
        url = f"{API_URL}/channels/967526705088565248/messages"
        res = requests.post(url, data=msg, headers=self.headers)
        res = json.loads(res.text)

        print(f'{res}\n')

    def check_msg(self):
        pass

    def response(self, event):
        role = Role()
        bool = role.set_role(event)
        role_id = event['d']['data']['custom_id']

        interaction_id = event['d']['id']
        interaction_token = event['d']['token']

        url = f"{API_URL}/interactions/{interaction_id}/{interaction_token}/callback"

        if bool == True:
            # when role has been added 
            response = {
                "type":4,
                "data":{
                    "tts":False,
                    "content": f"👍 You've now got the role `{role_id}`!",
                    "flags":64,
                    "embeds": [],
                    "allowed_mentions": { "parse": [] }
                }
            }
            msg = json.dumps(response)
            res = requests.post(url, data=msg, headers=self.headers)
            res = json.loads(res.text)

            print(f'{res}\n')

        else:
            # when role has been removed
            response = {
                "type":4,
                "data":{
                    "tts":False,
                    "content": f"🙃 I've removed the role `{role_id}` from you!",
                    "flags":64,
                    "embeds": [],
                    "allowed_mentions": { "parse": [] }
                }
            }
            msg = json.dumps(response)
            res = requests.post(url, data=msg, headers=self.headers)
            res = json.loads(res.text)

            print(f'{res}\n')

# this means some one clicked on a botton to choose a role
#  select a role
# return
# then respond
