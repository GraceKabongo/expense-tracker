from typing import List
from fastapi import HTTPException
from services.db import categorie_session
from schemas.categorieSchema import CategorieSchemaIn, CategorieSchemaOut
from models.categorieModel import Categorie
from services.db import categorie_session
from uuid import UUID
from sqlmodel import select
from datetime import datetime


def create_new_categorie(data: CategorieSchemaIn) -> CategorieSchemaOut:

    new_categorie = Categorie(**data.model_dump())
    with categorie_session:
        categorie_session.add(new_categorie)
        categorie_session.commit()
        categorie_session.refresh(new_categorie)
    
    return CategorieSchemaOut(
        id = str(new_categorie.id),
        name= new_categorie.name,
        created_at=new_categorie.created_at,
        updated_at=new_categorie.updated_at
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
                    name=categorie.name,
                    created_at= categorie.created_at,
                    updated_at= categorie.updated_at
                    ))   
    
    except Exception as e:
        raise e

    return data



def get_categorie(id:str) -> CategorieSchemaOut:
    
    try:
        with categorie_session:
            statement = select(Categorie).where(Categorie.id == UUID(id))
            categorie = categorie_session.exec(statement=statement).first()
            
            if categorie is None:
                raise HTTPException(404, "invalid id") 
    
    except Exception as e:
        print(e)
        raise HTTPException(500, "server error")

    return CategorieSchemaOut(
                    id=str(categorie.id),
                    name=categorie.name,
                    created_at= categorie.created_at,
                    updated_at= categorie.updated_at
                    )


def update_categorie(id: str, data: CategorieSchemaIn) -> CategorieSchemaOut:
    try:
        with categorie_session:
            statement = select(Categorie).where(Categorie.id == UUID(id))
            categorie = categorie_session.exec(statement=statement).first()
            
            if categorie is None:
                raise HTTPException(404, "invalid id") 

            if data.name != None:
                categorie.name = data.name
            
            categorie.updated_at = datetime.now()

            categorie_session.add(categorie)
            categorie_session.commit()
            categorie_session.refresh(categorie)
            
    
    except Exception as e:
        print(e)
        raise HTTPException(500, f"{e}")
    
    return CategorieSchemaOut(
                    id=str(categorie.id),
                    name=categorie.name,
                    created_at= categorie.created_at,
                    updated_at= categorie.updated_at
                    )


def delete_categorie(id:str) -> CategorieSchemaOut:
    try:
        with categorie_session:
            statement = select(Categorie).where(Categorie.id == UUID(id))
            categorie = categorie_session.exec(statement=statement).first()
            
            if categorie is None:
                raise HTTPException(404, "invalid id") 

            categorie_session.delete(categorie)
            categorie_session.commit()
            
    
    except Exception as e:
        print(e)
        raise HTTPException(500, f"{e}")
    
    return CategorieSchemaOut(
                    id=str(categorie.id),
                    name=categorie.name,
                    created_at= categorie.created_at,
                    updated_at= categorie.updated_at
                    )
