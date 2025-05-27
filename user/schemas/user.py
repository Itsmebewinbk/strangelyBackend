from pydantic import BaseModel,EmailStr,HttpUrl,Field

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password is required and must be at least 6 characters long")
    profile_pic: HttpUrl | None = None


class UserUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    profile_pic: HttpUrl | None = None



class GetUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    profile_pic: HttpUrl | None = None