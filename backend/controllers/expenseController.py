from schemas.expenseSchema import ExpenseSchema
from services.db import expense_session, categorie_session
from models.expenseModel import Expense
from models.categorieModel import Categorie
from fastapi import HTTPException
from sqlmodel import select
from uuid import UUID

def create_new_expense(data: ExpenseSchema, user_id: str):
    try:

        if data is None:
            raise HTTPException(422, "empty data") #TODO: error for empty data 
        
        if data.is_recurring:
            if data.start_date is None or data.end_date is None:
                raise HTTPException(400, "missing start or end date")
        
        #check if the categorie exist
        with categorie_session:
            statement = select(Categorie).where(Categorie.id == UUID(data.categorie_id))
            categorie = categorie_session.exec(statement=statement).first()
            
            if categorie is None:
                raise HTTPException(404, "invalid categorie") 

        data.user_id = user_id
        new_expense = Expense(**data.model_dump())

        with expense_session:
            expense_session.add(new_expense)
            expense_session.commit()
            expense_session.refresh(new_expense)

    except Exception as e :
        print(e)
        raise e
    
    return ExpenseSchema(**new_expense.model_dump())