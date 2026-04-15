from fastapi import Depends, Query, APIRouter, Body
from schemas.employee_schema import CreateEmployeeDTO, EmployeeDTO, UpdateEmployeeDTO
from services.employee_service import (
    get_employees_by_company,
    create_employee_func,
    get_employee_by_id,
    update_employee_by_id,
    delete_employee_by_id,
    get_employee_date,
)
from config.db import get_db
from schemas.response_schema import ResponseModel
from schemas.pagination_schema import PaginatedData
from schemas.status_schema import StatusEnum
from schemas.token_schema import TokenData
from services.auth_service import get_current_user

router = APIRouter(prefix="/employee", tags=["employee"], dependencies=[Depends(get_current_user)])

@router.post(
    "",
    response_model=ResponseModel[None],
    status_code=201,
    response_model_exclude_none=True,
)
async def create_employee(employee: CreateEmployeeDTO, db=(Depends(get_db))):
    return create_employee_func(db, emp=employee)

@router.get(
    "",
    response_model=ResponseModel[PaginatedData[EmployeeDTO]],
    status_code=200,
    response_model_exclude_none=True,
)
def get_all_employees(
    companyName: str = Query("", pattern="^[a-zA-Z]+$"),
    status: StatusEnum | None = Query(default="A"),
    pageLimit: int = Query(default=5),
    pageNo: int = Query(default=1),
    db=(Depends(get_db)),
):
    return get_employees_by_company(db, companyName, status, pageLimit, pageNo)

@router.get(
    "/date",
    response_model=ResponseModel[PaginatedData[EmployeeDTO]],
    status_code=200,
    response_model_exclude_none=True,
)
def get_employees_by_date(
    start_date: str = Query(),
    end_date: str = Query(),
    pageLimit: int = Query(default=5),
    pageNo: int = Query(default=1),
    db=(Depends(get_db)),
):
    return get_employee_date(db, start_date, end_date, pageLimit, pageNo)

@router.get(
    "/{employee_guid}",
    response_model=ResponseModel[EmployeeDTO],
    status_code=200,
    response_model_exclude_none=True,
)
def get_employee_by_guid(employee_guid: str, db=(Depends(get_db))):
    return get_employee_by_id(db, employee_guid)

@router.patch(
    "/{employee_guid}",
    response_model=ResponseModel[None],
    status_code=201,
    response_model_exclude_none=True,
)
async def update_employee(
    employee_guid: str, employee: UpdateEmployeeDTO = Body(), db=(Depends(get_db))
):
    return update_employee_by_id(db, employee_guid, employee)

@router.delete(
    "/{employee_guid}",
    response_model=ResponseModel[None],
    status_code=200,
    response_model_exclude_none=True,
)
async def delete_employee(employee_guid: str, db=(Depends(get_db))):
    return delete_employee_by_id(db, employee_guid)