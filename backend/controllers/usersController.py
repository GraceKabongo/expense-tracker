from models.userModel import User
from schemas.userSchema import UserSchemaIn, UserSchemaOut, UserSchemaUpdate
from services.db import user_session
from fastapi import HTTPException
from sqlmodel import select
from uuid import UUID
from bcrypt import gensalt, hashpw

def create_new_user(data: UserSchemaIn) -> UserSchemaOut:
    try:
        #password hashing
        password = data.password.encode()
        salt= gensalt()
        hashed_password = hashpw(password, salt)


        # create a new user
        new_user = User(first_name=data.firstname, last_name=data.lastname, email=data.email, password=hashed_password.decode())
        with user_session:
            user_session.add(new_user)
            user_session.commit()
            user_session.refresh(new_user)
    
    except Exception as e:
        user_session.rollback() # Rollback on error
        raise HTTPException(422, "email already taken")#TODO : implement Custom exception in the case where the email is taken       
    #except HTTPException as eh:
        #print(eh) #TODO: error for empty data
    
    return UserSchemaOut(
        id         = str(new_user.id),
        firstname  = new_user.first_name,
        lastname   = new_user.last_name,
        email      = new_user.email,
        password   = new_user.password,
        created_at = new_user.created_at,
        updated_at = new_user.updated_at
        )


def get_user(id: str) -> UserSchemaOut:
    with user_session:
        statement = select(User).where(User.id == UUID(id))
        user = user_session.exec(statement=statement).first()
        if user is None:
            raise HTTPException(404, "invalid id") #TODO custom error
        
        return UserSchemaOut(
            id         = str(user.id),
            firstname  = user.first_name,
            lastname   = user.last_name,
            email      = user.email,
            password   = user.password,
            created_at = user.created_at,
            updated_at = user.updated_at
        )


def update_user(id: str, data):
    pass


def delete_user():
    pass