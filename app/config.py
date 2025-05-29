from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    # aws_access_key: str
    # aws_secret_key: str
    # aws_bucket_name: str
    # aws_region: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  # Load .env

settings = Settings()
