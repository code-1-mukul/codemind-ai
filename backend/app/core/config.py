from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_VERSION: str
    HOST: str
    PORT: int
    UPLOAD_DIR: str
    FAISS_STORAGE_DIR: str = "storage/faiss"
    METADATA_STORAGE_DIR: str = "storage/metadata"
    GEMINI_API_KEY: str
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()