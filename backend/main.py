from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from routes import categories, user, expenses
from services import db

#database
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(db.engine)
    yield



app = FastAPI(lifespan=lifespan)
prefix = "/api"



app.include_router(categories.router, prefix=prefix)
app.include_router(expenses.router, prefix=prefix)
app.include_router(user.router, prefix=prefix)

@app.get("/")
def hello():
    return {"hello" : "world"}