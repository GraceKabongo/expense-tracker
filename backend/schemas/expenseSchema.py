from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class ExpenseSchema(BaseModel):
    id: Optional[UUID] = None
    amount: float 
    description: str
    categorie_id: str
    user_id: Optional[str] = None
    is_recurring: Optional[bool]= Field(default=False)
    start_date: Optional[datetime] = Field(default=None, nullable=True)
    end_date: Optional[datetime] = Field(default=None, nullable=True)
    created_at: datetime
    updated_at: datetime


class ExpenseSchemaUpdate(BaseModel):
    amount: Optional[float]        = None
    description: Optional[str]     = None
    categorie_id: Optional[str]    = None
    is_recurring: Optional[bool]   = False
    start_date: Optional[datetime] = None
    end_date: Optional[datetime]   = None