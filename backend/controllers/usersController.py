from models.userModel import User
from schemas.userSchema import UserSchemaIn, UserSchemaOut, UserSchemaUpdate
from services.db import user_session
from utils.utils import is_email_taken
from fastapi import HTTPException
from sqlmodel import select
from uuid import UUID
from utils.utils import hash_password


def create_new_user(data: UserSchemaIn) -> UserSchemaOut:
    try:
        if data is None:
            raise HTTPExceptiona(422, "empty data") #TODO: error for empty data
        
        # create a new user
        new_user = User(first_name=data.firstname, last_name=data.lastname, email=data.email, password=hash_password(data.password))
        with user_session:
            user_session.add(new_user)
            user_session.commit()
            user_session.refresh(new_user)
    
    except Exception as e:
        user_session.rollback() # Rollback on error
        print(e)
        raise HTTPException(422, "email already taken")#TODO : implement Custom exception in the case where the email is taken       

    
    return UserSchemaOut(
        id         = str(new_user.id),
        firstname  = new_user.first_name,
        lastname   = new_user.last_name,
        income     = new_user.income,
        email      = new_user.email,
        password   = new_user.password,
        created_at = new_user.created_at,
        updated_at = new_user.updated_at
        )


def get_user(id: str) -> UserSchemaOut:

    try:
        with user_session:
            statement = select(User).where(User.id == UUID(id))
            user = user_session.exec(statement=statement).first()
            if user is None:
                raise HTTPException(404, "invalid id") #TODO custom error
    
    except Exception:
        raise HTTPException(404, "invalid id")
    
    return UserSchemaOut(
        id         = str(user.id),
        firstname  = user.first_name,
        lastname   = user.last_name,
        email      = user.email,
        income     = user.income,
        password   = user.password,
        created_at = user.created_at,
        updated_at = user.updated_at
    )


def update_user(id: str, data: UserSchemaUpdate):
    try:
        with user_session:

            statement = select(User).where(User.id == UUID(id))
            user = user_session.exec(statement=statement).first()

            if user is None :
                raise HTTPException(404, "invalid id")
            if is_email_taken(user_session, data.email):
                raise HTTPException(422, 'Email taken')
            

            if data.email != None:
                user.email = data.email
            if data.firstname != None:
                user.first_name = data.firstname   
            if data.lastname != None:
                user.last_name = data.lastname
            if data.income != None:
                user.income = data.income
                
        
            user_session.add(user)
            user_session.commit()
            user_session.refresh(user)

    except Exception as e :
        raise HTTPException(404, "invalid id")
            

    return UserSchemaOut(
            id         = str(user.id),
            firstname  = user.first_name,
            lastname   = user.last_name,
            email      = user.email,
            income     = user.income,
            password   = user.password,
            created_at = user.created_at,
            updated_at = user.updated_at
        )

    


def delete_user(id:str):
    try:
        with user_session:

            statement = select(User).where(User.id == UUID(id))
            user = user_session.exec(statement=statement).first()

            if user is None :
                raise HTTPException(404, "invalid id")
            
            user_session.delete(user)
            user_session.commit()
    
    except Exception as e:
        raise HTTPException(404, "invalid id")

    return UserSchemaOut(
            id         = str(user.id),
            firstname  = user.first_name,
            lastname   = user.last_name,
            email      = user.email,
            income     = user.income,
            password   = user.password,
            created_at = user.created_at,
            updated_at = user.updated_at
        )
