from fastapi import FastAPI

from application.api.contract.handlers import router as contract_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Solana Smart Contract Bridge",
        docs_url='/api/docs',
        description="Service service that automatically generates, analyzes, \
            and deploys smart contracts to the Solana test network.",
    )
    app.include_router(contract_router, prefix='/contract')
    return app
