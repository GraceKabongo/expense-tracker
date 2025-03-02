from fastapi import FastAPI
from sqlmodel import SQLModel
from routes import categories, user, expenses
from services import db


app = FastAPI()
prefix = "/api"

#database
#SQLModel.metadata.create_all(db.engine)


app.include_router(categories.router, prefix=prefix)
app.include_router(expenses.router, prefix=prefix)
app.include_router(user.router, prefix=prefix)

@app.get("/")
def hello():
    return {"hello" : "world"}