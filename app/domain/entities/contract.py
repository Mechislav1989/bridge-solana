from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from domain.values.contract import (
    Code, ContractStatus, ProgramID, StatusType, CodeParams
)


@dataclass
class Contract:
    id: UUID
    code: Code | None
    status: ContractStatus
    program_id: ProgramID | None
    errors: tuple[str, ...]
    params: CodeParams

    @classmethod
    def create_new(cls, params: CodeParams) -> 'Contract':
        return cls(
            id=uuid4(),
            code=None,
            status=ContractStatus(StatusType.PENDING, timestamp=datetime.utcnow()),
            program_id=None,
            errors=(),
            params=params
        )

    def update_code(self, new_code: Code) -> None:
        self.code = new_code
        self.status = self.status.transition_to(StatusType.GENERATED)