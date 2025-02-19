from dataclasses import dataclass
import hashlib

from domain.values.contract import CodeParams


@dataclass(frozen=True)
class StaticPromptTemplate:
    BASE_TEMPLATE = """
    Generate a Solana smart contract in Rust for {purpose}.
    Requirements:
    - Use anchor framework v0.28.0
    - No unsafe code
    - Add input validation for all functions
    - Include error handling with custom error codes for common validation cases
    - Implement logic for {purpose} or other tokens
    - Add unit tests for initialization, minting, and validation functions
    - Include all necessary Anchor attributes like `#[account]`, `#[program]`, and `#[derive(Accounts)]`
    
    Please return only the Rust code, without explanations or extra text.

    Example structure:
    use anchor_lang::prelude::*;
    use std::str::FromStr;
    
    declare_id!({program_id});
    
    #[program]
    pub mod {module_name} {{
        // ... logic
    }}
    """

    @classmethod
    def build(cls, params: CodeParams) -> str:
        temp_id = cls.generate_program_id(params.contract_name)
        return cls.BASE_TEMPLATE.format(
            purpose=params.contract_type,
            program_id=temp_id,
            module_name=params.contract_name.lower()
        )

    @staticmethod
    def generate_program_id(name: str) -> str:
        return hashlib.sha256(name.encode()).hexdigest()[:32]