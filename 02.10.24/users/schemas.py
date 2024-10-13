from pydantic import BaseModel, Field
from typing import Optional

class SAuth(BaseModel):
    username: str
    password: str

class SCreate(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = Field(default=False)