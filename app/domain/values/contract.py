import base58
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re

from domain.values.base import BaseValueObject
from domain.exceptions.contract import (
    RustCodeException, InvalidStatusTransitionError, ProgramIDException,
    InvalidSeverity, InvalidNetwork
)


@dataclass(frozen=True)
class Code(BaseValueObject[str]):
    value: str

    def validate(self):    
        if not self._is_valid_rust_code():
            raise RustCodeException

    def _is_valid_rust_code(self) -> bool:
        return True if self.value.startswith('use anchor_lang') else False

    @classmethod
    def from_ai_response(cls, raw_text: str) -> 'Code':
        cleaned = re.sub(r'```(?:rust|.*)', '', raw_text)
        cleaned = re.sub(r'```', '', cleaned)
        cleaned = re.sub(r'###.*?\n', '', cleaned)

        cleaned = '\n'.join(line for line in cleaned.splitlines() if line.strip())
        cleaned = cleaned.strip()
        
        return cls(cleaned)

    def as_generic_type(self) -> str:
        return self.value


class StatusType(Enum):
    PENDING = 'pending'
    GENERATED = 'generated'
    ANALYZED = 'analyzed'
    DEPLOYED = 'deployed'
    FAILED = 'failed'


@dataclass(frozen=True)
class ContractStatus(BaseValueObject[StatusType]):
    value: StatusType
    timestamp: datetime

    def validate(self):
        allowed_transitions: dict[StatusType, list[StatusType]] = {
            StatusType.PENDING: [StatusType.GENERATED, StatusType.FAILED],
            StatusType.GENERATED: [StatusType.ANALYZED, StatusType.FAILED],
            StatusType.ANALYZED: [StatusType.DEPLOYED, StatusType.FAILED],
            StatusType.DEPLOYED: [],
            StatusType.FAILED: [],
        }
        if self.value not in allowed_transitions:
            raise InvalidStatusTransitionError()

    def transition_to(self, status: StatusType) -> 'ContractStatus':
        return ContractStatus(status, timestamp=datetime.utcnow)

    def as_generic_type(self) -> StatusType:
        return self.value


@dataclass(frozen=True)
class ProgramID(BaseValueObject[str]):
    value: str

    def validate(self):
        if not self._is_valid_solana_program_id():
            raise ProgramIDException

    def _is_valid_solana_program_id(self) -> bool:
        try:
            # Solana program ID is base58 encoded 32-byte array
            decoded = base58.b58decode(self.value)
            return len(decoded) == 32
        except Exception:
            return False

    def as_generic_as_type(self) -> str:
        return self.value


@dataclass(frozen=True)
class ValidationError(BaseValueObject[dict]):
    tool: str
    error_code: str
    message: str
    line: int
    severity: str  # "warning", "error", "critical"
    _value: dict = field(init=False)

    def validate(self):
        if self.severity not in {'warning', 'error', 'critical'}:
            raise InvalidSeverity(self.severity)

    def as_generic_type(self):
        ...


@dataclass(frozen=True)
class AnalysisResult:
    is_success: bool
    errors: list[ValidationError]


@dataclass(frozen=True)
class CodeParams(BaseValueObject[dict]):
    contract_type: str
    contract_name: str
    author: str = None
    network: str = "testnet"
    value: dict | None

    def validate(self):
        allowed = ['testnet', 'devnet', 'mainnet']
        if self.network not in allowed:
            raise InvalidNetwork(self.network)

    def as_generic_type(self):
        ...