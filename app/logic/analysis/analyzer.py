from abc import ABC, abstractmethod
import re
import subprocess
import tempfile

from domain.values.contract import (
    Code, AnalysisResult, ValidationError
)



class StaticAnalyzerInterface(ABC):
    @abstractmethod
    def analyze(self, code: Code) -> AnalysisResult:
        pass

    @abstractmethod
    def auto_fix(self, code: Code, errors: list) -> Code:
        pass


class ClippyAnalyzer(StaticAnalyzerInterface):
    def analyze(self, code) -> AnalysisResult:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                self._create_cargo_project(tmpdir, code.value)
                subprocess.run(
                    ["cargo", "clippy", "--all-targets", "--", "-D", "warnings"],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return AnalysisResult(success=True)
                
        except subprocess.CalledProcessError as e:
            errors = self._parse_errors(e.stderr)
            return AnalysisResult(success=False, errors=errors)

    def _parse_errors(self, output: str) -> list[ValidationError]:
        errors = []
        pattern = r"error: (.*)\n --> .*:(\d+):\d+"
        matches = re.findall(pattern, output)
        
        for msg, line in matches:
            errors.append(
                ValidationError(
                    tool="clippy",
                    error_code="CLIPPY_ERR",
                    message=msg,
                    line=int(line),
                    severity="error"
                )
            )
        return errors

    def auto_fix(self, code, errors):
        ...    


class PrustiAnalyzer(StaticAnalyzerInterface):
    def analyze(self, code: str) -> AnalysisResult:
        try:
            subprocess.run(
                ["prusti-rustc", "--edition=2021"], 
                input=code,
                capture_output=True,
                text=True,
                check=True
            )
            return AnalysisResult(True)
        except subprocess.CalledProcessError as e:
            errors = self._parse_prusti_output(e.stderr)
            return AnalysisResult(False, errors)

    def _parse_errors(self, output: str) -> list[ValidationError]:
        errors = []
        pattern = r"\[Prusti\] (Error|Warning): (.*) at line (\d+)"
        
        for match in re.finditer(pattern, output):
            severity = match.group(1).lower()
            message = match.group(2)
            line = int(match.group(3))
            
            errors.append(
                ValidationError(
                    tool="prusti",
                    error_code="PRUSTI_ERR",
                    message=message,
                    line=line,
                    severity=severity
                )
            )
        return errors

    def auto_fix(self, code, errors):
        ...