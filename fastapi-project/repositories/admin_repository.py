from ..schemas.admin_schema import CreateAdminDTO
from sqlalchemy.orm import Session
from ..models.admin import Admin

def create_admin_repo(db: Session, admin: CreateAdminDTO, guid: str):
    db_admin = Admin(**admin.model_dump())
    db.add(db_admin, guid=guid)

def get_admin_by_email_repo(db: Session, email: str):
    result = db.query(Admin).filter(Admin.email == email).first()
    return result

def get_hashed_password_repo(db: Session, email: str):
    result = db.query(Admin.password_hash).filter(Admin.email == email).first()
    return result
