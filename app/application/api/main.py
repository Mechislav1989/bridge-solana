from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Solana Smart Contract Bridge",
        docs_url='/api/docs',
        description="Service service that automatically generates, analyzes, \
            and deploys smart contracts to the Solana test network.",
    )
    
    return app
