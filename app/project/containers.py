from functools import lru_cache
import punq

from infra.ai_client.open_ai import OpenAIAdapter

from project.configs.general import settings


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()
    
    def init_openai():
        return OpenAIAdapter(api_key=settings.OPENAI_API_KEY)
    
    container.register(OpenAIAdapter, factory=init_openai, scope=punq.Scope.singleton)
    
    return container
