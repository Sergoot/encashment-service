from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    atm_host: str
    algo_host: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra = "allow",
        env_prefix = "BFF_",
    )