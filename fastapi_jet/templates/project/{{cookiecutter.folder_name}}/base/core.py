from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(
        cls, value: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(value, str) and not value.startswith("["):
            return [item.strip() for item in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)


settings = Settings()
