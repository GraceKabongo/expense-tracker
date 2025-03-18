from fastapi import APIRouter
from schemas.expenseSchema import ExpenseSchema
from controllers.expenseController import create_new_expense
from models.userModel import User
from auth.authentication import get_current_user
from typing import Annotated
from fastapi import Depends

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)

@router.get("/")
def root():
    return "expense root "

@router.post("/create-expense")
def creat_expense(data: ExpenseSchema, user: Annotated[User, Depends(get_current_user)]):
    return create_new_expense(data, str(user.id))