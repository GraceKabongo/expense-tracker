from typing import List
from fastapi import HTTPException
from services.db import categorie_session
from schemas.categorieSchema import CategorieSchemaIn, CategorieSchemaOut
from models.categorieModel import Categorie
from services.db import categorie_session
from uuid import UUID
from sqlmodel import select


def create_new_categorie(data: CategorieSchemaIn) -> CategorieSchemaOut:

    new_categorie = Categorie(name=data.name)
    with categorie_session:
        categorie_session.add(new_categorie)
        categorie_session.commit()
        categorie_session.refresh(new_categorie)
    
    return CategorieSchemaOut(
        id = str(new_categorie.id),
        name= new_categorie.name
    ) 


def get_all_categorie() -> List[CategorieSchemaOut]:
    data = []
    try:
        with categorie_session:
            statement = select(Categorie)
            categories = categorie_session.exec(statement=statement).all()
            for categorie in categories:
                data.append(CategorieSchemaOut(
                    id=str(categorie.id),
                    name=categorie.name
                    ))   
    
    except Exception as e:
        print(e)
        raise HTTPException(500, "server error")

    return data



def get_categorie(id:str) -> CategorieSchemaOut:
    
    try:
        with categorie_session:
            statement = select(Categorie).where(Categorie.id == UUID(id))
            categorie = categorie_session.exec(statement=statement).first()
            
            if categorie is None:
                raise HTTPException(404, "invalid id") #TODO custom error
    
    except Exception as e:
        print(e)
        raise HTTPException(500, "server error")

    return CategorieSchemaOut(
        id=str(categorie.id),
        name= categorie.name
    )
    
    