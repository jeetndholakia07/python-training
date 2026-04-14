from ..schemas.company_schema import CreateCompanyDTO, UpdateCompanyDTO
from ..utils.guid import generateGUID, is_valid_guid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas.status_schema import StatusEnum
from ..repositories.company_respository import (
    create_company_repo,
    get_all_company_repo,
    get_company_by_id_repo,
    update_company_desc_repo,
    delete_company_by_id_repo,
    get_company_id_repo,
    get_company_status_repo,
    get_company_by_name_repo,
)

def create_company_func(db: Session, company: CreateCompanyDTO):
    try:
        if company.status not in ["A", "D"]:
            raise HTTPException(status_code=400, detail="Invalid status format")
        check_company_by_name(db, company.companyName)
        guid = generateGUID()
        create_company_repo(db, company, guid)
        db.commit()
        return {"success": True, "message": "Company created successfully"}
    except Exception:
        db.rollback()
        raise

def get_companies(
    db: Session, status: StatusEnum | None, pageLimit: int = 5, pageNo: int = 1
):
    try:
        pageLimit = int(pageLimit)
        pageNo = int(pageNo)
        offset = (pageNo - 1) * pageLimit
        results = get_all_company_repo(db, status, pageLimit, offset)
        return {
            "success": True,
            "data": {
                "page": pageNo,
                "limit": pageLimit,
                "data": results.get("data"),
                "totalItems": results.get("totalItems"),
            },
        }
    except Exception:
        raise

def get_company_by_id(db: Session, companyGuid: str):
    try:
        if not is_valid_guid(companyGuid):
            raise HTTPException(status_code=400, detail="Invalid GUID")
        result = get_company_by_id_repo(db, companyGuid)
        if result is None:
            raise HTTPException(status_code=404, detail="Company not found")
        return {"success": True, "data": result}
    except Exception:
        raise

def update_company_desc(db: Session, companyGuid: str, company: UpdateCompanyDTO):
    try:
        if not is_valid_guid(companyGuid):
            raise HTTPException(status_code=400, detail="Invalid GUID")
        companyId = get_company_id(db, companyGuid)
        update_company_desc_repo(db, company, companyId)
        db.commit()
        return {"success": True, "message": "Company updated successfully"}
    except Exception:
        db.rollback()
        raise

def delete_company_by_id(db: Session, companyGuid: str):
    try:
        if not is_valid_guid(companyGuid):
            raise HTTPException(status_code=400, detail="Invalid GUID")
        companyId = get_company_id(db, companyGuid)
        delete_company_by_id_repo(db, companyId)
        db.commit()
        return {"success": True, "message": "Company deleted successfully"}
    except Exception:
        db.rollback()
        raise

def get_company_id(db: Session, companyGuid: str):
    result = get_company_id_repo(db, companyGuid)
    if result is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return result[0]

def check_company_active(db: Session, companyGuid: str):
    result = get_company_status_repo(db, companyGuid)
    if result is None:
        raise HTTPException(status_code=404, detail="Company not found")
    if result[0] == "D":
        raise HTTPException(status_code=400, detail="Invalid company")

def check_company_by_name(db: Session, name: str):
    result = get_company_by_name_repo(db, name)
    if result is not None:
        raise HTTPException(status_code=400, detail="Company already exists")