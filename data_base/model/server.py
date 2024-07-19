from pydantic import BaseModel

class Server(BaseModel):
    id: str
    prefix: str
    mute_role: None | int
    level_channel: None | str
    shop: dict
    channelW: None | str
    messageW: None | str
    autoroleW: None | str
    imageurlW: None | str
    channelG: None | str
    messageG: None | str
    autoroleG: None | str
    imageurlG: None | str