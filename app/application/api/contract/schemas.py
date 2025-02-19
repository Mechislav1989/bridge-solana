from pydantic import BaseModel
from typing import Optional

from domain.entities.contract import Contract
from domain.values.contract import CodeParams


class ContractCreateRequest(BaseModel):
    prompt: Optional[str] = None
    params: CodeParams


class ContractResponse(BaseModel):
    id: str
    status: str
    code: str
    errors: list[str] = []

    @classmethod
    def from_entity(cls, contract: 'Contract') -> 'ContractResponse':
        return cls(
            id=str(contract.id),
            status=contract.status,
            code=contract.code.as_generic_type(),
            errors=contract.errors
        )

class ErrorSchema(BaseModel):
    error: str