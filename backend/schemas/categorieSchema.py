from pydantic import BaseModel, Field
from datetime import datetime


class CategorieSchemaIn(BaseModel):
    name : str = Field(min_length=3, max_length=80)


class CategorieSchemaOut(BaseModel):
    id: str
    name : str
    created_at: datetime
    updated_at: datetime