from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExpenseSchema(BaseModel):
    amount: float 
    description: str
    categorie_id: str
    user_id: Optional[str] = None
    is_recurring: Optional[bool]= Field(default=False)
    start_date: Optional[datetime] = Field(default=None, nullable=True)
    end_date: Optional[datetime] = Field(default=None, nullable=True)