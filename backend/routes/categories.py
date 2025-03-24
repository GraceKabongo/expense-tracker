from fastapi import APIRouter, Depends
from controllers.categorieController import create_new_categorie, get_all_categorie, get_categorie, update_categorie, delete_categorie
from schemas.categorieSchema import CategorieSchemaIn, CategorieSchemaOut
from typing import Annotated, List
from models.userModel import User
from auth.authentication import get_current_user


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)



@router.post("/create-categorie", response_model=CategorieSchemaOut)
def create_categorie(data: CategorieSchemaIn, _: Annotated[User, Depends(get_current_user)]):
    categorie = create_new_categorie(data=data)
    return categorie


@router.get("/", response_model=List[CategorieSchemaOut])
def fetch_all_categorie(_: Annotated[User, Depends(get_current_user)]):
    return get_all_categorie() 


@router.get("/{id}", response_model=CategorieSchemaOut)
def fetch_categorie(id:str, _: Annotated[User, Depends(get_current_user)]):
    return get_categorie(id)


@router.put("/update-categorie/{id}", response_model=CategorieSchemaOut)
def edit_categorie(id:str, data: CategorieSchemaIn, _: Annotated[User, Depends(get_current_user)]):
    return update_categorie(id, data)


@router.delete("/delete-categorie/{id}", response_model=CategorieSchemaOut)
def remove_categorie(id:str, _: Annotated[User, Depends(get_current_user)]):
    return delete_categorie(id)