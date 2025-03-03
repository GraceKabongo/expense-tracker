from sqlmodel import create_engine, Session



sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"
#backend/database.db

engine = create_engine(sqlite_url, echo=False)

user_session = Session(engine)