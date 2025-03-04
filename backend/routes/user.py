from fastapi import APIRouter
from uuid import UUID
from schemas.userSchema import UserSchemaIn, UserSchemaOut, UserSchemaUpdate
from controllers.usersController import create_new_user, get_user, update_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/")
def root():
    return "users root "


@router.post("/create-user", response_model=UserSchemaOut)
def create_user(data: UserSchemaIn):
    user = create_new_user(data=data)
    return user


@router.get("/{id}", response_model=UserSchemaOut) #TODO: once auth implemented no need of using id paramater
def fetch_user(id: str):
    return get_user(id)



@router.put("/{id}") #TODO: once auth implemented no need of using id paramater
def edit_user(id: str, data: UserSchemaUpdate):
    return update_user(id, data)


