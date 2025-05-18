from typing import Generic, TypeVar, Optional
from app.schemas import StandardResponse

T = TypeVar("T")


def standard_response(data=None, message: str = "", status: str = "success"):
    return StandardResponse(status=status, message=message, result=data)
