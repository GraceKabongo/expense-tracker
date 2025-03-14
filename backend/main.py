from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from routes import categories, user, expenses
from auth.routes import auth
from services import db
from dotenv import load_dotenv


load_dotenv()

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
app.include_router(auth.router, prefix=prefix)

@app.get("/")
def hello():
    return {"hello" : "world"}