# check if some one is has role , then change

from info import get
from message import API_URL
from info import get, save

class Select_Role:
    def __init__(self,role,user):
        info = get()
        self.guild_id = info["guild_id"]
        self.role = role
        pass
    # check if in role then remove
    # else add to role
    # check if role exists if not then make role
    def get_role():



