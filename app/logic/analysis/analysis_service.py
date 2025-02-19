from dataclasses import dataclass

from domain.values.contract import AnalysisResult, ValidationError
from logic.analysis.analyzer import StaticAnalyzerInterface


@dataclass
class AnalysisService:
    analyzers: list[StaticAnalyzerInterface]

    def analyze(self, code: str) -> AnalysisResult:
        all_errors = []
        all_warnings = []
        
        for analyzer in self.analyzers:
            result = analyzer.analyze(code)
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)
        
        return AnalysisResult(
            is_success=len(all_errors) == 0,
            errors=all_errors,
        )

    def auto_fix(self, code: str, errors: list[ValidationError]) -> str:
        fixes = []
        for error in errors:
            if error.tool == "clippy":
                fixes.append(f"// FIX: {error.message}\n// Original line {error.line}")
            elif error.tool == "prusti":
                fixes.append(f"// PRUSTI FIX: {error.message}")
        
        return code + "\n\n// Auto-fixes:\n" + "\n".join(fixes)