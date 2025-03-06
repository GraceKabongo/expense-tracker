from fastapi import APIRouter
from controllers.categorieController import create_new_categorie, get_all_categorie, get_categorie
from schemas.categorieSchema import CategorieSchemaIn, CategorieSchemaOut
from typing import List


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)



@router.post("/create-categorie", response_model=CategorieSchemaOut)
def create_categorie(data: CategorieSchemaIn):
    categorie = create_new_categorie(data=data)
    return categorie


@router.get("/", response_model=List[CategorieSchemaOut])
def fetch_all_categorie():
    return get_all_categorie() 


@router.get("/{id}", response_model=CategorieSchemaOut)
def fetch_categorie(id:str):
    return get_categorie(id)