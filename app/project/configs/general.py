from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PYTHONPATH: str
    OPENAI_API_KEY: str
    
    model_config = SettingsConfigDict(env_file='.env', encoding='utf-8', env_nested_delimiter='\n')


settings = Settings()