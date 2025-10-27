from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    phone_country_code: str


class UsersOut(BaseModel):
    users: Optional[List[UserOut]]
