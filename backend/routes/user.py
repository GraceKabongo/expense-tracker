from fastapi import APIRouter, HTTPException
from models.userModel import User
from schemas.userSchema import UserSchemaIn, UserSchemaOut
from services.db import session

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/")
def root():
    return "users root "


@router.post("/create-user", response_model=UserSchemaOut)
def create_user(data: UserSchemaIn):
    try:
        new_user = User(first_name=data.firstname, last_name=data.lastname, email=data.email, password=data.password)
        with session:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
    except Exception as e:
        session.rollback() # Rollback on error
        print("Email already taken") #TODO : implement Custom exception in the case where the email is taken
    except HTTPException as eh:
        print(eh) #TODO: error for empty data
    return UserSchemaOut(
        id=str(new_user.id),
        firstname=new_user.first_name,
        lastname=new_user.last_name,
        email=new_user.email,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at
        )