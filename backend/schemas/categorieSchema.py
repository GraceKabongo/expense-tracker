from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CategorieSchemaIn(BaseModel):
    name : str = Field(min_length=3, max_length=80)


class CategorieSchemaOut(BaseModel):
    id: str
    name : str
    created_at: Optional[datetime]= None
    updated_at: Optional[datetime] = None