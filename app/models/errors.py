from pydantic import BaseModel


class NotFound(BaseModel):
    error: str = "Resource not found"
