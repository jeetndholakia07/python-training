from schemas.employee_schema import CreateEmployeeDTO, UpdateEmployeeDTO
from utils.guid import generateGUID, is_valid_guid
from services.company_service import get_company_id
from fastapi import HTTPException
from schemas.status_schema import StatusEnum
from repositories.employee_repository import (
    create_employee_repo,
    get_employees_repo,
    get_employee_by_id_repo,
    update_employee_id_repo,
    delete_employee_by_id_repo,
    get_employee_id_repo,
    get_employee_date_repo,
)
from .company_service import check_company_active
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

def create_employee_func(db: Session, emp: CreateEmployeeDTO):
    try:
        if emp.status not in ["A", "D"]:
            raise HTTPException(status_code=400, detail="Invalid status format")
        companyId = get_company_id(db, emp.companyGuid)
        check_company_active(db, emp.companyGuid)
        guid = generateGUID()
        create_employee_repo(db, emp, companyId, guid)
        db.commit()
        return {"success": True, "message": "Employee created successfully"}
    except Exception:
        db.rollback()
        raise

def get_employees_by_company(
    db: Session,
    companyName: str,
    status: StatusEnum | None = None,
    pageLimit: int = 5,
    pageNo: int = 1,
):
    try:
        pageLimit = int(pageLimit)
        pageNo = int(pageNo)
        offset = (pageNo - 1) * pageLimit
        results = get_employees_repo(db, pageLimit, offset, companyName, status)
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

def get_employee_by_id(db: Session, empGuid: str):
    try:
        if not is_valid_guid(empGuid):
            raise HTTPException(status_code=400, detail="Invalid GUID")
        result = get_employee_by_id_repo(db, empGuid)
        if result is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"success": True, "data": result}
    except Exception:
        raise

def update_employee_by_id(db: Session, empGuid: str, emp: UpdateEmployeeDTO):
    try:
        if not is_valid_guid(empGuid):
            raise HTTPException(status_code=400, detail="Invalid GUID")
        employeeId = get_employee_id(db, empGuid)
        update_employee_id_repo(db, emp, employeeId)
        db.commit()
        return {"success": True, "message": "Employee updated successfully"}
    except Exception:
        db.rollback()
        raise

def delete_employee_by_id(db: Session, empGuid: str):
    try:
        if not is_valid_guid(empGuid):
            raise HTTPException(status_code=400, detail="Invalid GUID")
        employeeId = get_employee_id(db, empGuid)
        delete_employee_by_id_repo(db, employeeId)
        db.commit()
        return {"success": True, "message": "Employee deleted successfully"}
    except Exception:
        db.rollback()
        raise

def get_employee_id(db: Session, empGuid: str):
    result = get_employee_id_repo(db, empGuid)
    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result[0]

def get_employee_date(
    db: Session, startDate: str, endDate: str, pageLimit: int = 5, pageNo: int = 1
):
    pageLimit = int(pageLimit)
    pageNo = int(pageNo)
    offset = (pageNo - 1) * pageLimit
    start_dt = datetime.strptime(startDate, "%d-%m-%Y")
    end_dt = datetime.strptime(endDate, "%d-%m-%Y") + timedelta(days=1)
    results = get_employee_date_repo(db, start_dt, end_dt, pageLimit, offset)
    return {
        "success": True,
        "data": {
            "page": pageNo,
            "limit": pageLimit,
            "data": results.get("data"),
            "totalItems": results.get("totalItems"),
        },
    }