from sqlmodel import create_engine, Session



sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"


engine = create_engine(sqlite_url, echo=False)

#sessions
user_session = Session(engine)
categorie_session = Session(engine)