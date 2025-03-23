from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class Categorie(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name : str = Field(min_length=3, max_length=120, unique=True)
    created_at : datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at : datetime = Field(default_factory=datetime.now, nullable=False)