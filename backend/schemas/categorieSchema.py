from pydantic import BaseModel, Field


class CategorieSchemaIn(BaseModel):
    name : str = Field(min_length=3, max_length=80)


class CategorieSchemaOut(BaseModel):
    id: str
    name : str