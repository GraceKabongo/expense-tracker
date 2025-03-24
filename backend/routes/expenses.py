from fastapi import APIRouter
from schemas.expenseSchema import ExpenseSchema, ExpenseSchemaUpdate
from controllers.expenseController import create_new_expense, get_expense, get_all_expense, update_expense, delete_expense
from models.userModel import User
from auth.authentication import get_current_user
from typing import Annotated, List
from fastapi import Depends

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)


@router.get("/{id}", response_model=ExpenseSchema)
def fetch_one_expense(id: str):
    return get_expense(id)



@router.get("/", response_model=List[ExpenseSchema])
def fetch_all_expense(user: Annotated[User, Depends(get_current_user)]):
    return get_all_expense(str(user.id))


@router.post("/create-expense", response_model=ExpenseSchema)
def creat_expense(data: ExpenseSchema, user: Annotated[User, Depends(get_current_user)]):
    return create_new_expense(data, str(user.id))

@router.put("/update-expense/{id}", response_model=ExpenseSchema)
def modify_expense(id: str, data: ExpenseSchemaUpdate, _: Annotated[User, Depends(get_current_user)]):
    return update_expense(id=id, data=data)

@router.delete("/delete-expense/{id}", response_model=ExpenseSchema)
def remove_expense(id: str, _: Annotated[User, Depends(get_current_user)]):
    return delete_expense(id)