from pydantic import BaseModel

class Server(BaseModel):
    id: str
    prefix: str
    mute_role: int | None
    channelW: str | None
    messageW: str | None
    autoroleW: str | None
    imageurlW: str | None
    channelG: str |None
    messageG: str | None
    autoroleG: str | None
    imageurlG: str | None