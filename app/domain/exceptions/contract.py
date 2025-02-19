from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class RustCodeException(ApplicationException):
    @property
    def message(self):
        return 'Invalid Rust Code'


dataclass(eq=False)
class InvalidStatusTransitionError(ApplicationException):
    ...


dataclass(eq=False)
class ProgramIDException(ApplicationException):
    ...


@dataclass(eq=False)
class InvalidSeverity(ApplicationException):
    severity: str
    
    @property
    def message(self):
        return f'InvalidSeverity: {self.severity}'


@dataclass(eq=False)
class InvalidNetwork(ApplicationException):
    allowed: list[str]
    
    @property
    def message(self):
        return f'Network must be one of {self.allowed}'