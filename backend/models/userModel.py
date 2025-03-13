from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from models.expenseModel import Expense

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name : str = Field(min_length=3, max_length=24)
    last_name :str = Field(min_length=3, max_length=24)
    email : str = Field(unique=True)
    password: str
    created_at : datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at : datetime = Field(default_factory=datetime.now, nullable=False)

    