from sqlmodel import Session, select
from models.userModel import User
from bcrypt import gensalt, hashpw

def is_email_taken(session: Session, email: str) -> bool:
    existing_user = session.exec(select(User).where(User.email == email)).first()
    return existing_user is not None


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt() ).decode()