from schemas.user_schema import CreateUserDTO
from sqlalchemy.orm import Session
from models.user import User

def create_admin_repo(db: Session, admin: CreateUserDTO, guid: str):
    db_user = User(**admin.model_dump(include={"username", "email", "role"}))
    db_user.password_hash = admin.password
    db_user.guid = guid
    db.add(db_user)

def get_user_by_email_repo(db: Session, email: str):
    result = (
        db.query(User.email, User.guid, User.username, User.role)
        .filter(User.email == email)
        .first()
    )
    if result:
        return {
            "email": result.email,
            "userGuid": result.guid,
            "username": result.username,
            "role": result.role,
        }
    return None

def get_hashed_password_repo(db: Session, email: str):
    result = db.query(User.password_hash).filter(User.email == email).first()
    return result