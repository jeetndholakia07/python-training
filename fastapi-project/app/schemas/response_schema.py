from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str | None = None