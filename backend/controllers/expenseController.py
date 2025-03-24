from schemas.expenseSchema import ExpenseSchema, ExpenseSchemaUpdate
from services.db import expense_session, categorie_session
from models.expenseModel import Expense
from models.categorieModel import Categorie
from fastapi import HTTPException
from sqlmodel import select
from uuid import UUID
from datetime import datetime

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
        raise e
    
    return ExpenseSchema(**new_expense.model_dump())



def get_expense(id: str):
    
    try:
        with expense_session:
            statement = select(Expense).where(Expense.id == UUID(id))
            expense = expense_session.exec(statement=statement).first()

            if expense is None:
                raise HTTPException(404, "invalid ID")

    except Exception as e:
        raise e

    return ExpenseSchema(**expense.model_dump())


def get_all_expense(user_id: str):
    try:
        with expense_session:
            statement = select(Expense).where(Expense.user_id == user_id)
            expenses = expense_session.exec(statement=statement).all()


    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))

    return [ExpenseSchema(**expense.model_dump()) for expense in expenses]


def update_expense(id:str, data: ExpenseSchemaUpdate):
    try:
        with expense_session, categorie_session:
            
            statement = select(Expense).where(Expense.id == UUID(id))
            expense = expense_session.exec(statement=statement).first()

            if expense is None:
                raise HTTPException(404, "this expense does not exist")
            
            # check if the new categorie exist
            if data.categorie_id != None:
                statement = select(Categorie).where(Categorie.id == UUID(data.categorie_id))
                categorie = categorie_session.exec(statement=statement).first()

                if categorie is None:
                    raise HTTPException(400, "this categorie does not exist")
                
                expense.categorie_id = str(categorie.id)
            
            # assign new data if provided
            if data.amount != None:
                expense.amount = data.amount
            if data.description != None:
                expense.description = data.description

            # check if the expense is recurring and provide start and end date
            if data.is_recurring:
                if data.start_date is None or data.end_date is None:
                    raise HTTPException(400, "the start and end date must be provided")
                
                expense.is_recurring = True
                expense.start_date = data.start_date
                expense.end_date = data.end_date
            
            expense.updated_at = datetime.now()
            
            expense_session.add(expense)
            expense_session.commit()
            expense_session.refresh(expense)

    except Exception as e:
        raise e

    return ExpenseSchema(**expense.model_dump())


def delete_expense(id: str):
    try:
        with expense_session:
            statement = select(Expense).where(Expense.id == UUID(id))
            expense = expense_session.exec(statement=statement).first()

            if expense is None:
                raise HTTPException(404, "expense cannot be found")
            
            expense_session.delete(expense)
            expense_session.commit()

    except Exception as e :
        raise e
    
    return Expense(**expense.model_dump())