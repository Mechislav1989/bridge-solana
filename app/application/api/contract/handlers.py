
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from application.api.contract.schemas import (
    ContractCreateRequest, ContractResponse, ErrorSchema
)
from domain.entities.contract import Contract
from domain.exceptions.base import ApplicationException
from infra.ai_client.open_ai import OpenAIAdapter
from logic.generation.generation_service import GenerationService
from logic.generation.static_prompt import StaticPromptTemplate

from project.containers import get_container


router = APIRouter(tags=['Smart Contract'])

def get_generation_service():
    container = get_container()
    ai_client = container.resolve(OpenAIAdapter)
    generation_service = GenerationService(ai_client, StaticPromptTemplate)
    return generation_service


def process_contract_generation(
    contract: Contract, service: GenerationService, prompt = None
    ) -> Contract:
    contract = service.generate(contract.params)
    contract.status = "generated"
    return contract


@router.post(
    '/',
    response_model=ContractResponse,
    status_code=status.HTTP_201_CREATED,
    description='',
    responses={
        status.HTTP_201_CREATED: {'model': ContractResponse},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    }
)
async def create_contract(
    request: ContractCreateRequest,
    service: GenerationService = Depends(get_generation_service)
):
    try:
        contract = Contract.create_new(request.params)
        
        contract_code = process_contract_generation( 
            contract,
            service,
            request.prompt
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    
    return ContractResponse.from_entity(contract_code)