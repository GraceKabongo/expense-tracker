from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class Categorie(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name : str = Field(min_length=3, max_length=120)