from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str

    URL_RATE_API: str


    @property
    def rabbitmq_url(self) -> str:
        return (
            f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@'
            f'{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}'
        )


    @property
    def redis_url(self) -> str:
        return (
            f'redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:'
            f'{self.REDIS_PORT}/{self.REDIS_DB}'
        )


    @property
    def url_rate_api(self) -> str:
        return self.URL_RATE_API


settings = Settings()
