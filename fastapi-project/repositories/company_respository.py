from ..schemas.company_schema import CreateCompanyDTO, UpdateCompanyDTO
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.company import Company

def create_company_repo(db: Session, company: CreateCompanyDTO, guid: str):
    data = company.model_dump(include={"companyName", "description", "status"})
    db_company = Company(**data, guid=guid)
    db.add(db_company)

def get_all_company_repo(db: Session, status, limit, offset):
    query = db.query(Company)
    if status is not None:
        query = query.filter(Company.status == status)
    total_count = query.with_entities(func.count()).scalar()
    companies = query.offset(offset).limit(limit).all()
    data = [
        {
            "companyName": c.companyName,
            "description": c.description,
            "status": c.status,
            "companyGuid": c.guid,
        }
        for c in companies
    ]

    return {"data": data, "totalItems": total_count}

def get_company_by_id_repo(db: Session, companyGuid: str):
    company = db.query(Company).filter(Company.guid == companyGuid).first()
    if not company:
        return None
    return {
        "companyName": company.companyName,
        "description": company.description,
        "status": company.status,
        "companyGuid": company.guid,
    }

def update_company_desc_repo(db: Session, company: UpdateCompanyDTO, companyId):
    db_company = db.query(Company).filter(Company.id == companyId).first()
    if db_company:
        db_company.description = company.description

def delete_company_by_id_repo(db: Session, companyId):
    db_company = db.query(Company).filter(Company.id == companyId).first()
    if db_company:
        db_company.status = "D"

def get_company_id_repo(db: Session, companyGuid: str):
    result = db.query(Company.id).filter(Company.guid == companyGuid).first()
    return result

def get_company_status_repo(db: Session, companyGuid: str):
    result = db.query(Company.status).filter(Company.guid == companyGuid).first()
    return result

def get_company_by_name_repo(db: Session, name: str):
    result = db.query(Company).filter(Company.companyName == name).first()
    return result