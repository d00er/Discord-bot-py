from pydantic import BaseModel

class User(BaseModel):
    id: str
    level: int
    experience: int
    balance= int
    deposit= int
    objects= dict