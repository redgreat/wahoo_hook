from pydantic import BaseModel


class GetUser(BaseModel):
    user: str
