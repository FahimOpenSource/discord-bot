from info import get
from info import get, save
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

API_URL = "https://discord.com/api/v9"


class Role:
    def __init__(self):
        info = get()
        self.guild_id = info["guild_id"]
        self.token = os.getenv("TOKEN")
        self.headers = {"Authorization": f"Bot {self.token}", "Content-Type": "application/json"}

    def set_role(self, event):

        # Get guild roles
        url = f"{API_URL}/guilds/{self.guild_id}/roles"
        res = requests.get(url, headers=self.headers)
        print(f'from setrole {res.text}\n')
        roles = json.loads(res.text)

        # Check if roles include the given
        id = event['d']['data']['custom_id']
        for role in roles:
            name = role["name"]
            if name == id:
                return self.assign_role(event, role)
            else:
                # The role doesn't exist
                # Send message : Role unavailable
                pass
    
    def assign_role(self, event, role):
        role_id = role['id']
        user_id = event['d']['member']['user']['id']

        # get member object
        url = f"{API_URL}/guilds/{self.guild_id}/members/{user_id}"
        res = requests.get(url, headers=self.headers)
        print(f'user {res.text}\n')
        member = json.loads(res.text)

        print(f'role selected by user {role}\n')

        # does program check whether user has role before removing or adding it

        # removing role
        if role['id'] in member["roles"]:
            url = f"{API_URL}/guilds/{self.guild_id}/members/{user_id}/roles/{role_id}"
            res = requests.delete(url, headers=self.headers)
            print(f'role deleted{res.text}\n')
            assert res.status_code == 204
            return False
            
        else:
            # adding role to user
            url = f"{API_URL}/guilds/{self.guild_id}/members/{user_id}/roles/{role_id}"
            res = requests.put(url, headers=self.headers)
            print(f'role added {res.text}\n')
            assert res.status_code == 204
            return True 
        
  