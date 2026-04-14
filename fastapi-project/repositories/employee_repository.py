from schemas.employee_schema import CreateEmployeeDTO, UpdateEmployeeDTO
from schemas.status_schema import StatusEnum
from sqlalchemy.orm import Session
from models.employee import Employee
from sqlalchemy import func

def create_employee_repo(db: Session, emp: CreateEmployeeDTO, companyId, guid):
    data = emp.model_dump(
        include={"employeeName", "designation", "salary", "status"}
    )
    db_employee = Employee(**data, guid=guid, companyId=companyId)
    db.add(db_employee)

def get_employees_repo(
    db: Session, limit, offset, companyName: str, status: StatusEnum | None
):
    query = db.query(Employee, Employee.company).join(Employee.company)
    if companyName:
        query = query.filter(Employee.company.has(companyName=companyName))
    if status:
        query = query.filter(Employee.status == status)
    total_count = query.with_entities(func.count()).scalar()
    employees = query.offset(offset).limit(limit).all()
    data = [
        {
            "employeeName": emp.employeeName,
            "designation": emp.designation,
            "salary": emp.salary,
            "employeeGuid": emp.guid,
            "companyName": emp.company.companyName,
            "status": emp.status,
        }
        for emp in employees
    ]
    return {"data": data, "totalItems": total_count}

def get_employee_by_id_repo(db: Session, empGuid: str):
    emp = (
        db.query(Employee)
        .join(Employee.company)
        .filter(Employee.guid == empGuid)
        .first()
    )
    if not emp:
        return None
    return {
        "employeeName": emp.employeeName,
        "designation": emp.designation,
        "salary": emp.salary,
        "employeeGuid": emp.guid,
        "companyName": emp.company.companyName,
        "status": emp.status,
    }

def update_employee_id_repo(db: Session, emp: UpdateEmployeeDTO, employeeId):
    db_employee = db.query(Employee).filter(Employee.id == employeeId).first()
    if db_employee:
        db_employee.designation = emp.designation

def delete_employee_by_id_repo(db: Session, employeeId):
    db_employee = db.query(Employee).filter(Employee.id == employeeId).first()
    if db_employee:
        db_employee.status = "D"

def get_employee_id_repo(db: Session, empGuid: str):
    result = db.query(Employee.id).filter(Employee.guid == empGuid).first()
    return result[0] if result else None

def get_employee_date_repo(db: Session, startDate: str, endDate: str, limit, offset):
    query = (
        db.query(Employee)
        .join(Employee.company)
        .filter(Employee.updatedAt >= startDate, Employee.updatedAt < endDate)
    )
    total_count = query.with_entities(func.count()).scalar()
    employees = query.offset(offset).limit(limit).all()
    data = [
        {
            "employeeName": emp.employeeName,
            "designation": emp.designation,
            "salary": emp.salary,
            "employeeGuid": emp.guid,
            "companyName": emp.company.companyName,
            "status": emp.status,
        }
        for emp in employees
    ]
    return {"data": data, "totalItems": total_count}