from typing import Annotated
from fastapi import APIRouter, Depends
from uuid import UUID
from schemas.userSchema import UserSchemaIn, UserSchemaOut, UserSchemaUpdate
from controllers.usersController import create_new_user, get_user, update_user, delete_user
from models.userModel import User
from auth.authentication import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)



@router.post("/create-user", response_model=UserSchemaOut)
def create_user(data: UserSchemaIn):
    user = create_new_user(data=data)
    return user


@router.get("/", response_model=UserSchemaOut) #TODO: once auth implemented no need of using id paramater
def fetch_user(current_user: Annotated[User, Depends(get_current_user)]):
    return get_user(str(current_user.id))



@router.put("/{id}") #TODO: once auth implemented no need of using id paramater
def edit_user(id: str, data: UserSchemaUpdate):
    return update_user(id, data)


@router.delete("/{id}") #TODO: once auth implemented no need of using id paramater
def remove_user(id: str):
    return delete_user(id)