from sqlmodel import Field, SQLModel
from datetime import datetime
from uuid import UUID, uuid4



class Expense(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    amount: float
    description: str
    date: datetime = Field(default_factory=datetime.now, nullable=False)
    is_recurring: bool = Field(default=False)
    start_date: datetime = Field(default=None, nullable=True)
    end_date: datetime = Field(default=None, nullable=True)
    created_at : datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at : datetime = Field(default_factory=datetime.now, nullable=False)

    categorie_id: str | None = Field(default=None, foreign_key="categorie.id")
    user_id: str | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE")