from fastapi import APIRouter, Depends, Query, Body
from app.services.company_service import (
    create_company_func,
    get_companies,
    get_company_by_id,
    update_company_desc,
    delete_company_by_id,
)
from app.core.config import get_db
from app.schemas.company_schema import CreateCompanyDTO, CompanyDTO, UpdateCompanyDTO
from app.schemas.status_schema import StatusEnum
from app.schemas.response_schema import ResponseModel
from app.schemas.pagination_schema import PaginatedData
from app.schemas.user_schema import Role
from app.services.auth_service import get_current_user, require_roles

router = APIRouter(prefix="/company", tags=["company"])

@router.post(
    "",
    response_model=ResponseModel[None],
    status_code=201,
    response_model_exclude_none=True,
)
async def create_company(
    company: CreateCompanyDTO,
    db=(Depends(get_db)),
    current_user=Depends(require_roles(Role.A, Role.C)),
):
    return create_company_func(db, company)

@router.get(
    "",
    response_model=ResponseModel[PaginatedData[CompanyDTO]],
    status_code=200,
    response_model_exclude_none=True,
)
def get_all_companies(
    status: StatusEnum | None = Query(default=None, examples="A"),
    pageLimit: int = Query(default=5),
    pageNo: int = Query(default=1),
    db=(Depends(get_db)),
    current_user=Depends(get_current_user),
):
    return get_companies(db, status, pageLimit, pageNo)

@router.get(
    "/{company_guid}",
    response_model=ResponseModel[CompanyDTO],
    status_code=200,
    response_model_exclude_none=True,
)
def get_company_by_guid(
    company_guid: str, db=(Depends(get_db)), current_user=Depends(get_current_user)
):
    return get_company_by_id(db, company_guid)

@router.patch(
    "/{company_guid}",
    response_model=ResponseModel[None],
    status_code=201,
    response_model_exclude_none=True,
)
async def update_company(
    company_guid: str,
    company: UpdateCompanyDTO = Body(),
    db=(Depends(get_db)),
    current_user=Depends(require_roles(Role.A, Role.C)),
):
    return update_company_desc(db, company_guid, company)

@router.delete(
    "/{company_guid}",
    response_model=ResponseModel[None],
    status_code=200,
    response_model_exclude_none=True,
)
async def delete_company(
    company_guid: str,
    db=(Depends(get_db)),
    current_user=Depends(require_roles(Role.A, Role.C)),
):
    return delete_company_by_id(db, company_guid)