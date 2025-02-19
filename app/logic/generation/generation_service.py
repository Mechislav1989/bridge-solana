from dataclasses import dataclass

from domain.entities.contract import Contract
from domain.values.contract import CodeParams
from infra.ai_client.open_ai import OpenAIAdapter
from logic.generation.static_prompt import StaticPromptTemplate


@dataclass
class GenerationService:
    ai_client: OpenAIAdapter
    # repo: ContractRepository
    prompt_template: StaticPromptTemplate
        
    def generate(
        self, params: CodeParams, custom_prompt: str | None = None
    ) -> Contract:
        prompt = custom_prompt or self.prompt_template.build(params)
        code = self.ai_client.generate_code(prompt)
        contract = Contract.create_new(params)
        contract.update_code(code)
        # self.repo.save(contract)
        return contract