from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional
from datetime import datetime


class UserSchemaIn(BaseModel):
    firstname : str = Field(min_length=3, max_length=24)
    lastname: str =  Field(min_length=3, max_length=24)
    email: EmailStr
    password : str = Field(min_length=6, max_length=1024)


class UserSchemaOut(BaseModel):
    id: str
    firstname : str
    lastname: str  
    email: EmailStr
    income: float
    password: Annotated[str, Field(exclude=True)]
    created_at: Optional[datetime]= None
    updated_at: Optional[datetime] = None


class UserSchemaUpdate(BaseModel):
    firstname : Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    income: Optional[float] = 0