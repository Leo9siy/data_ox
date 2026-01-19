from pydantic import Field
from pydantic.v1 import BaseSettings
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    POSTGRES_USER: str = Field(default="user")
    POSTGRES_PASSWORD: str = Field(default="password")
    POSTGRES_NAME: str = Field(default="db")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default="5432")

    @property
    def DATABASE_URL(self):
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=self.POSTGRES_NAME
        ).unicode_string()

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
