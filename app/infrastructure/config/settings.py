from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = 8000

    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB_NAME: str = 'postgres'
    DB_PORT: int = 5432

    SECRET_KEY: str = '4146b14f6b88f0e94042309d523279c8490446e74f3669062466721304207296'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379

    RABBITMQ_PORT: int = 5672
    RABBITMQ_HOST: str = 'localhost'
    RABBITMQ_USER: str = 'guest'
    RABBITMQ_PASSWORD: str = 'guest'

    MAIN_API_URL: str = '/api/v1'

    BASE_CRYPTO_URL: str = 'https://api.binance.com/api/v3/ticker/price'
    MAIN_CURRENCY: str = 'USDT'

    @property
    def postgres_url(self):
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
            f'{self.DB_PORT}/{self.POSTGRES_DB_NAME}'
        )

    @property
    def test_db_url(self):
        return 'sqlite+aiosqlite:///db.sqlite3'

    @property
    def rabbitmq_url(self):
        return f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/'

    @property
    def redis_url(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
