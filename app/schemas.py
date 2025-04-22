
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Annotated
from pydantic.types import conint

# chats
class Chat(BaseModel):
    content: str
class PromptRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    role: str
    content: str

class ChatHistory(BaseModel):
    role: str
    content: str
    memory: dict
    

# users

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int

    class Config:
        from_attributes = True

class UserPostResponse(BaseModel):
    email: EmailStr
    id: int
    class Config:
        from_attributes = True


# auth
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
