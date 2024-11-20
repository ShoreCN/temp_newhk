from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    code: int = 200
    message: str = "Success"
    data: Optional[T] = None
    meta: Optional[dict] = None
    
class ErrorResponse(BaseModel):
    code: int
    message: str
    details: Optional[Any] = None 