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


@router.get("/", response_model=UserSchemaOut) 
def fetch_user(current_user: Annotated[User, Depends(get_current_user)]):
    return get_user(str(current_user.id))



@router.put("/update-user") 
def edit_user(current_user: Annotated[User, Depends(get_current_user)], data: UserSchemaUpdate):
    return update_user(str(current_user.id), data)


@router.delete("/delete-user") 
def remove_user(current_user: Annotated[User, Depends(get_current_user)]):
    return delete_user(str(current_user.id))