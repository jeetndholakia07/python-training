from schemas.admin_schema import CreateAdminDTO
from sqlalchemy.orm import Session
from models.admin import Admin

def create_admin_repo(db: Session, admin: CreateAdminDTO, guid: str):
    db_admin = Admin(**admin.model_dump(include={"username","email"}))
    db_admin.password_hash = admin.password
    db_admin.guid = guid
    db.add(db_admin)

def get_admin_by_email_repo(db: Session, email: str):
    result = db.query(Admin).filter(Admin.email == email).first()
    return result

def get_hashed_password_repo(db: Session, email: str):
    result = db.query(Admin.password_hash).filter(Admin.email == email).first()
    return result