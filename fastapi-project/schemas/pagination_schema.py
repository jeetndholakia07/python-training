from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class PaginatedData(BaseModel, Generic[T]):
    page: int
    limit: int
    data: List[T]
    totalItems:int