"""
Base settings for tapir.
"""
import sys
from pathlib import Path

from pydantic import (
    BaseSettings,
    DirectoryPath,
    Field,
    ValidationError,
    validator,
)
from rich import print as rprint

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent


class Settings(BaseSettings):
    root: DirectoryPath = Field(Path.home() / ".tapir", env="TAPIR_HOME")
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    @validator("root", pre=True)
    def root_must_exist(cls, path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        return path

    class Config:
        env_file = Path.home() / ".tapir" / ".env"


try:
    settings = Settings()  # type: ignore
except ValidationError as e:
    rprint("validation error: ", e)
    sys.exit(1)
